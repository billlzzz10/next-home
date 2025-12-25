import { SearchResponse, Document } from '../types.js';
import { EmbeddingService } from './embedding-service.js';
import { CostCalculator } from './cost-calculator.js';
import { UserLogger } from '../utils/user-logger.js';
import { FilterOptions } from '../utils/filters.js';

export class SearchEngine {
  private embeddingService: EmbeddingService;
  private costCalculator: CostCalculator;
  private logger: UserLogger;
  private documents: Document[] = [];

  constructor(
    embeddingService: EmbeddingService,
    costCalculator: CostCalculator,
    logger: UserLogger
  ) {
    this.embeddingService = embeddingService;
    this.costCalculator = costCalculator;
    this.logger = logger;
  }

  addDocuments(docs: Document[]): void {
    this.documents.push(...docs);
  }

  async search(
    query: string,
    userId: string,
    filters: FilterOptions = {},
    topK: number = 5,
    scoreThreshold: number = 0.82,
    useRerank: boolean = true
  ): Promise<SearchResponse> {
    const startTime = Date.now();

    this.logger.log({
      type: 'search_request',
      method: 'search',
      params: {
        query: query.substring(0, 200),
        topK,
        scoreThreshold,
        useRerank
      },
      userId
    });

    try {
      // 1. Create embedding
      const { embedding, tokens: embeddingTokens } = await this.embeddingService.createEmbedding(query);
      const embeddingCost = this.costCalculator.calculateEmbeddingCost(embeddingTokens);

      // 2. Simple vector search (mock)
      let searchResults = this.simpleSearch(query, topK * 2);

      // 3. Rerank if needed
      let rerankCost = 0;
      let rerankUsed = false;

      if (useRerank && searchResults.length > 0) {
        const { results } = await this.embeddingService.rerank(
          query,
          searchResults.map(r => r.content)
        );
        searchResults = results.map((r, idx) => ({
          id: r.id,
          score: r.score,
          content: r.content,
          metadata: searchResults[idx]?.metadata
        }));
        rerankUsed = true;
        rerankCost = this.costCalculator.calculateRerankCost(100);
      }

      // 4. Filter by score threshold
      const filteredResults = searchResults
        .filter(result => result.score >= scoreThreshold)
        .slice(0, topK);

      // 5. Determine if LLM is needed
      const shouldUseLLM = filteredResults.length === 0;

      // 6. Calculate total cost
      const totalCost = embeddingCost + rerankCost;
      const totalTokens = embeddingTokens + (rerankUsed ? 100 : 0);

      // 7. Log results
      this.logger.log({
        type: 'search_result',
        method: 'search',
        result: {
          resultCount: filteredResults.length,
          costEstimate: totalCost,
          tokens: totalTokens
        },
        userId,
        metadata: {
          embeddingProvider: this.embeddingService.getProvider(),
          rerankUsed,
          processingTime: Date.now() - startTime
        }
      });

      return {
        results: filteredResults,
        total: filteredResults.length,
        costEstimate: totalCost,
        tokensUsed: totalTokens,
        shouldUseLLM,
        rerankUsed,
        provider: this.embeddingService.getProvider()
      };
    } catch (error) {
      this.logger.log({
        type: 'error',
        method: 'search',
        error: error instanceof Error ? error.message : 'Unknown error',
        userId
      });

      throw error;
    }
  }

  private simpleSearch(query: string, limit: number) {
    const queryLower = query.toLowerCase();
    const results = this.documents
      .map(doc => ({
        id: doc.id,
        score: this.calculateSimilarity(queryLower, doc.content.toLowerCase()),
        content: doc.content,
        metadata: doc.metadata
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);

    return results;
  }

  private calculateSimilarity(query: string, content: string): number {
    const queryWords = query.split(/\s+/);
    const contentWords = content.split(/\s+/);

    let matches = 0;
    for (const word of queryWords) {
      if (contentWords.some(w => w.includes(word))) {
        matches++;
      }
    }

    return queryWords.length > 0 ? matches / queryWords.length : 0;
  }
}
