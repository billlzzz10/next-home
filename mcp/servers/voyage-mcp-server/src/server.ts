import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { Tool, TextContent, ErrorContent } from '@modelcontextprotocol/sdk/types.js';

import { QdrantVectorStore } from './vector-store/qdrant-store.js';
import { EmbeddingService } from './services/embedding-service.js';
import { CostCalculator } from './services/cost-calculator.js';
import { SearchEngine } from './services/search-engine.js';
import { UserLogger } from './utils/user-logger.js';
import { ConfigManager } from './utils/config-manager.js';
import { AppConfig } from './types.js';

class MCPVoyageServer {
  private server: Server;
  private configManager: ConfigManager;
  private config: AppConfig;
  private embeddingService: EmbeddingService;
  private costCalculator: CostCalculator;
  private searchEngine: SearchEngine;
  private userLogger: UserLogger;

  constructor(configPath: string = 'config/default.yaml') {
    this.configManager = new ConfigManager(configPath);
    this.config = this.configManager.getAll();

    this.server = new Server(
      {
        name: 'voyage-mcp-server',
        version: '1.1.0'
      },
      {
        capabilities: {
          tools: {}
        }
      }
    );

    // Initialize logger
    this.userLogger = new UserLogger('default_user', this.config.logging.baseLogDir);

    // Initialize embedding service
    this.embeddingService = new EmbeddingService(
      this.config.providers.primary,
      {
        voyageApiKey: this.config.providers.voyage.apiKey,
        mistralApiKey: this.config.providers.mistral.apiKey
      }
    );

    // Initialize cost calculator
    this.costCalculator = new CostCalculator(
      this.config.cost.embeddingCostPerMillion,
      this.config.cost.rerankCostPerThousand,
      this.config.providers.primary,
      this.config.search.minTokensForRerank
    );

    // Initialize search engine
    this.searchEngine = new SearchEngine(
      this.embeddingService,
      this.costCalculator,
      this.userLogger
    );

    this.setupTools();

    // Rotate logs every 24 hours
    setInterval(() => {
      this.userLogger.rotateLogs(this.config.logging.rotateDays);
    }, 24 * 60 * 60 * 1000);
  }

  private setupTools(): void {
    // Tool 1: Search Documents
    this.server.setRequestHandler('tools/call', async (request) => {
      const tool = request.params.name;
      const args = request.params.arguments as Record<string, any>;

      try {
        if (tool === 'search_documents') {
          return {
            content: [
              {
                type: 'text' as const,
                text: JSON.stringify({
                  shouldUseLLM: true,
                  message: 'Search not configured - using LLM instead',
                  results: []
                })
              }
            ]
          };
        } else if (tool === 'estimate_cost') {
          const query = args.query as string;
          const useRerank = args.useRerank ?? true;

          const embeddingTokens = this.costCalculator.estimateTokens(query);
          const embeddingCost = this.costCalculator.calculateEmbeddingCost(embeddingTokens);
          const rerankCost = useRerank
            ? this.costCalculator.calculateRerankCost(
                this.costCalculator.getMinTokensForRerank()
              )
            : 0;

          this.userLogger.log({
            type: 'system',
            method: 'estimate_cost',
            params: { query: query.substring(0, 50), useRerank },
            metadata: {
              embeddingTokens,
              embeddingCost,
              rerankCost
            }
          });

          return {
            content: [
              {
                type: 'text' as const,
                text: JSON.stringify({
                  embeddingTokens,
                  embeddingCost: embeddingCost.toFixed(6),
                  rerankCost: rerankCost.toFixed(6),
                  totalCost: (embeddingCost + rerankCost).toFixed(6),
                  provider: this.config.providers.primary
                })
              }
            ]
          };
        } else if (tool === 'get_config') {
          return {
            content: [
              {
                type: 'text' as const,
                text: JSON.stringify(this.config, null, 2)
              }
            ]
          };
        } else if (tool === 'update_config') {
          const updates = args.updates as Partial<AppConfig>;
          const newConfig = this.configManager.update(updates);

          this.userLogger.log({
            type: 'system',
            method: 'update_config',
            result: { status: 'success' }
          });

          return {
            content: [
              {
                type: 'text' as const,
                text: JSON.stringify({
                  status: 'success',
                  message: 'Configuration updated',
                  config: newConfig
                })
              }
            ]
          };
        } else {
          throw new Error(`Unknown tool: ${tool}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify({
                error: error instanceof Error ? error.message : 'Unknown error'
              })
            }
          ]
        };
      }
    });

    // Tool 2: List available tools
    this.server.setRequestHandler('tools/list', () => {
      const tools: Tool[] = [
        {
          name: 'search_documents',
          description:
            'Search for documents in the vector database. Returns relevant documents or recommends using LLM if no good matches found.',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'The search query'
              },
              topK: {
                type: 'number',
                description: 'Number of results to return (default: 5)',
                default: 5
              },
              scoreThreshold: {
                type: 'number',
                description: 'Minimum similarity score (default: 0.82)',
                default: 0.82
              },
              useRerank: {
                type: 'boolean',
                description: 'Use AI reranking (default: true)',
                default: true
              },
              estimateOnly: {
                type: 'boolean',
                description: 'Only estimate cost without searching',
                default: false
              }
            },
            required: ['query']
          }
        },
        {
          name: 'estimate_cost',
          description: 'Estimate the cost of a search operation',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'The search query to estimate cost for'
              },
              useRerank: {
                type: 'boolean',
                description: 'Include rerank cost (default: true)',
                default: true
              }
            },
            required: ['query']
          }
        },
        {
          name: 'get_config',
          description: 'Get current server configuration',
          inputSchema: {
            type: 'object',
            properties: {}
          }
        },
        {
          name: 'update_config',
          description: 'Update server configuration',
          inputSchema: {
            type: 'object',
            properties: {
              updates: {
                type: 'object',
                description: 'Configuration updates to apply'
              }
            },
            required: ['updates']
          }
        }
      ];

      return {
        tools
      };
    });
  }

  async start(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);

    this.userLogger.log({
      type: 'system',
      method: 'server_start',
      metadata: {
        version: '1.1.0',
        provider: this.config.providers.primary,
        collection: this.config.qdrant.collectionName
      }
    });

    console.error(`[Voyage MCP Server] Started with provider: ${this.config.providers.primary}`);
  }
}

// Start server
const server = new MCPVoyageServer();
server.start().catch(console.error);
