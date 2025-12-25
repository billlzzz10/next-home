import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
  Tool,
  TextContent,
  ErrorResponse,
} from "@modelcontextprotocol/sdk/types.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios, { AxiosInstance } from "axios";

const BASE_URL = "https://connect.craft.do/links/4hD3qTwgwc1/api/v1";

interface CraftBlockInput {
  type?: string;
  id?: string;
  markdown?: string;
  textStyle?: string;
  [key: string]: any;
}

interface CraftPosition {
  position: "start" | "end" | "before" | "after";
  pageId?: string;
  targetBlockId?: string;
}

interface CraftSearchParams {
  documentId?: string;
  pattern?: string;
  caseSensitive?: boolean;
  beforeBlockCount?: number;
  afterBlockCount?: number;
}

class CraftAPIServer {
  private server: Server;
  private client: AxiosInstance;
  private tools: Tool[] = [];

  constructor() {
    this.server = new Server({
      name: "craft-api-mcp",
      version: "1.0.0",
    });

    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    this.setupTools();
    this.setupHandlers();
  }

  private setupTools(): void {
    this.tools = [
      {
        name: "list_documents",
        description:
          "Retrieve all documents accessible through the multi-document connection. Returns document IDs, titles, and deletion status.",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "get_blocks",
        description:
          "Fetch content from documents. Use to retrieve block content with nested children.",
        inputSchema: {
          type: "object",
          properties: {
            id: {
              type: "string",
              description:
                "The ID of the page/document/block to fetch (required)",
            },
            maxDepth: {
              type: "number",
              description:
                "Maximum depth of blocks to fetch. -1 = all descendants, 0 = only specified block, 1 = only direct children. Default: -1",
            },
            fetchMetadata: {
              type: "boolean",
              description:
                "Whether to fetch metadata (comments, createdBy, etc). Default: false",
            },
          },
          required: ["id"],
        },
      },
      {
        name: "insert_blocks",
        description:
          "Insert content into documents. Content can be provided as structured JSON blocks or markdown.",
        inputSchema: {
          type: "object",
          properties: {
            markdown: {
              type: "string",
              description: "Markdown content to insert",
            },
            blocks: {
              type: "array",
              description: "Array of block objects to insert",
              items: {
                type: "object",
              },
            },
            position: {
              type: "object",
              description: "Position to insert blocks",
              properties: {
                position: {
                  type: "string",
                  enum: ["start", "end", "before", "after"],
                  description: "Position relative to target",
                },
                pageId: {
                  type: "string",
                  description: "Document/page ID where to insert",
                },
                targetBlockId: {
                  type: "string",
                  description:
                    "Block ID for before/after positioning (optional)",
                },
              },
              required: ["position", "pageId"],
            },
          },
          required: ["position"],
          anyOf: [
            { required: ["markdown", "position"] },
            { required: ["blocks", "position"] },
          ],
        },
      },
      {
        name: "update_blocks",
        description:
          "Update content across documents. Only provided fields will be updated.",
        inputSchema: {
          type: "object",
          properties: {
            blocks: {
              type: "array",
              description: "Array of blocks with id and fields to update",
              items: {
                type: "object",
                properties: {
                  id: {
                    type: "string",
                    description: "Block ID to update",
                  },
                  markdown: {
                    type: "string",
                    description: "Updated markdown content",
                  },
                },
                required: ["id"],
              },
            },
          },
          required: ["blocks"],
        },
      },
      {
        name: "delete_blocks",
        description: "Delete content from documents by block IDs.",
        inputSchema: {
          type: "object",
          properties: {
            blockIds: {
              type: "array",
              items: {
                type: "string",
              },
              description: "Array of block IDs to delete",
            },
          },
          required: ["blockIds"],
        },
      },
      {
        name: "move_blocks",
        description:
          "Move blocks to reorder them or move them between documents.",
        inputSchema: {
          type: "object",
          properties: {
            blockIds: {
              type: "array",
              items: {
                type: "string",
              },
              description: "Array of block IDs to move",
            },
            position: {
              type: "object",
              description: "Target position",
              properties: {
                position: {
                  type: "string",
                  enum: ["start", "end", "before", "after"],
                },
                pageId: {
                  type: "string",
                  description: "Target document/page ID",
                },
                targetBlockId: {
                  type: "string",
                  description: "Target block ID for before/after",
                },
              },
              required: ["position", "pageId"],
            },
          },
          required: ["blockIds", "position"],
        },
      },
      {
        name: "search_document",
        description:
          "Search content within a single Craft document using regular expressions.",
        inputSchema: {
          type: "object",
          properties: {
            documentId: {
              type: "string",
              description: "The document ID to search within",
            },
            pattern: {
              type: "string",
              description: "Regular expression pattern to search for",
            },
            caseSensitive: {
              type: "boolean",
              description: "Whether search should be case sensitive. Default: false",
            },
            beforeBlockCount: {
              type: "number",
              description: "Number of blocks to include before matched block",
            },
            afterBlockCount: {
              type: "number",
              description: "Number of blocks to include after matched block",
            },
          },
          required: ["documentId", "pattern"],
        },
      },
      {
        name: "search_documents",
        description:
          "Search content across multiple documents using relevance-based ranking.",
        inputSchema: {
          type: "object",
          properties: {
            include: {
              type: "string",
              description: "Search terms to include (can be single string or array)",
            },
            documentIds: {
              type: "string",
              description:
                "Document IDs to filter (optional). If not provided, all documents searched.",
            },
            documentFilterMode: {
              type: "string",
              enum: ["include", "exclude"],
              description: "Whether to include or exclude specified documents. Default: include",
            },
          },
          required: ["include"],
        },
      },
      {
        name: "list_collections",
        description:
          "List all collections across documents in this multi-document connection",
        inputSchema: {
          type: "object",
          properties: {
            documentIds: {
              type: "array",
              items: {
                type: "string",
              },
              description:
                "Document IDs to filter. If not provided, all documents searched.",
            },
          },
        },
      },
      {
        name: "get_collection_schema",
        description: "Get the schema for a collection by its ID.",
        inputSchema: {
          type: "object",
          properties: {
            collectionId: {
              type: "string",
              description: "The unique ID of the collection",
            },
            format: {
              type: "string",
              description: "Format for schema. Default: json-schema-items",
            },
          },
          required: ["collectionId"],
        },
      },
      {
        name: "get_collection_items",
        description:
          "Retrieve all items from a specific collection.",
        inputSchema: {
          type: "object",
          properties: {
            collectionId: {
              type: "string",
              description: "The unique ID of the collection",
            },
          },
          required: ["collectionId"],
        },
      },
      {
        name: "add_collection_items",
        description: "Add new items to a specific collection.",
        inputSchema: {
          type: "object",
          properties: {
            collectionId: {
              type: "string",
              description: "The unique ID of the collection",
            },
            items: {
              type: "array",
              description: "Array of items to add",
              items: {
                type: "object",
                properties: {
                  title: {
                    type: "string",
                  },
                  properties: {
                    type: "object",
                  },
                },
              },
            },
          },
          required: ["collectionId", "items"],
        },
      },
      {
        name: "delete_collection_items",
        description: "Delete items from a specific collection by their IDs.",
        inputSchema: {
          type: "object",
          properties: {
            collectionId: {
              type: "string",
              description: "The unique ID of the collection",
            },
            idsToDelete: {
              type: "array",
              items: {
                type: "string",
              },
              description: "Array of item IDs to delete",
            },
          },
          required: ["collectionId", "idsToDelete"],
        },
      },
      {
        name: "update_collection_items",
        description: "Update existing items in a specific collection.",
        inputSchema: {
          type: "object",
          properties: {
            collectionId: {
              type: "string",
              description: "The unique ID of the collection",
            },
            itemsToUpdate: {
              type: "array",
              description: "Array of items to update (must include id)",
              items: {
                type: "object",
                properties: {
                  id: {
                    type: "string",
                  },
                  title: {
                    type: "string",
                  },
                  properties: {
                    type: "object",
                  },
                },
                required: ["id"],
              },
            },
          },
          required: ["collectionId", "itemsToUpdate"],
        },
      },
    ];
  }

  private setupHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: this.tools,
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request;

      try {
        const result = await this.handleToolCall(name, args as Record<string, unknown>);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        const errorMessage =
          error instanceof Error
            ? error.message
            : "Unknown error occurred";
        return {
          content: [
            {
              type: "text",
              text: `Error: ${errorMessage}`,
              isError: true,
            },
          ],
        } as ErrorResponse;
      }
    });
  }

  private async handleToolCall(
    toolName: string,
    args: Record<string, unknown>
  ): Promise<unknown> {
    switch (toolName) {
      case "list_documents":
        return this.listDocuments();

      case "get_blocks":
        return this.getBlocks(args);

      case "insert_blocks":
        return this.insertBlocks(args);

      case "update_blocks":
        return this.updateBlocks(args);

      case "delete_blocks":
        return this.deleteBlocks(args);

      case "move_blocks":
        return this.moveBlocks(args);

      case "search_document":
        return this.searchDocument(args);

      case "search_documents":
        return this.searchDocuments(args);

      case "list_collections":
        return this.listCollections(args);

      case "get_collection_schema":
        return this.getCollectionSchema(args);

      case "get_collection_items":
        return this.getCollectionItems(args);

      case "add_collection_items":
        return this.addCollectionItems(args);

      case "delete_collection_items":
        return this.deleteCollectionItems(args);

      case "update_collection_items":
        return this.updateCollectionItems(args);

      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }

  private async listDocuments(): Promise<unknown> {
    const response = await this.client.get("/documents");
    return response.data;
  }

  private async getBlocks(args: Record<string, unknown>): Promise<unknown> {
    const { id, maxDepth, fetchMetadata } = args;

    if (!id) {
      throw new Error("id parameter is required");
    }

    const params: Record<string, unknown> = {
      id,
      ...(maxDepth !== undefined && { maxDepth }),
      ...(fetchMetadata !== undefined && { fetchMetadata }),
    };

    const response = await this.client.get("/blocks", { params });
    return response.data;
  }

  private async insertBlocks(args: Record<string, unknown>): Promise<unknown> {
    const { markdown, blocks, position } = args;

    if (!position) {
      throw new Error("position parameter is required");
    }

    const body: Record<string, unknown> = {
      position,
    };

    if (markdown) {
      body.markdown = markdown;
    }

    if (blocks) {
      body.blocks = blocks;
    }

    if (!markdown && !blocks) {
      throw new Error("Either markdown or blocks parameter is required");
    }

    const response = await this.client.post("/blocks", body);
    return response.data;
  }

  private async updateBlocks(args: Record<string, unknown>): Promise<unknown> {
    const { blocks } = args;

    if (!blocks || !Array.isArray(blocks)) {
      throw new Error("blocks parameter is required and must be an array");
    }

    const response = await this.client.put("/blocks", { blocks });
    return response.data;
  }

  private async deleteBlocks(args: Record<string, unknown>): Promise<unknown> {
    const { blockIds } = args;

    if (!blockIds || !Array.isArray(blockIds)) {
      throw new Error("blockIds parameter is required and must be an array");
    }

    const response = await this.client.delete("/blocks", {
      data: { blockIds },
    });
    return response.data;
  }

  private async moveBlocks(args: Record<string, unknown>): Promise<unknown> {
    const { blockIds, position } = args;

    if (!blockIds || !Array.isArray(blockIds)) {
      throw new Error("blockIds parameter is required and must be an array");
    }

    if (!position) {
      throw new Error("position parameter is required");
    }

    const response = await this.client.put("/blocks/move", {
      blockIds,
      position,
    });
    return response.data;
  }

  private async searchDocument(
    args: Record<string, unknown>
  ): Promise<unknown> {
    const { documentId, pattern, caseSensitive, beforeBlockCount, afterBlockCount } =
      args;

    if (!documentId || !pattern) {
      throw new Error("documentId and pattern parameters are required");
    }

    const params: Record<string, unknown> = {
      documentId,
      pattern,
      ...(caseSensitive !== undefined && { caseSensitive }),
      ...(beforeBlockCount !== undefined && { beforeBlockCount }),
      ...(afterBlockCount !== undefined && { afterBlockCount }),
    };

    const response = await this.client.get("/blocks/search", { params });
    return response.data;
  }

  private async searchDocuments(
    args: Record<string, unknown>
  ): Promise<unknown> {
    const { include, documentIds, documentFilterMode } = args;

    if (!include) {
      throw new Error("include parameter is required");
    }

    const params: Record<string, unknown> = {
      include,
      ...(documentIds && { documentIds }),
      ...(documentFilterMode && { documentFilterMode }),
    };

    const response = await this.client.get("/documents/search", { params });
    return response.data;
  }

  private async listCollections(
    args: Record<string, unknown>
  ): Promise<unknown> {
    const { documentIds } = args;

    const params: Record<string, unknown> = {};
    if (documentIds) {
      params.documentIds = documentIds;
    }

    const response = await this.client.get("/collections", { params });
    return response.data;
  }

  private async getCollectionSchema(
    args: Record<string, unknown>
  ): Promise<unknown> {
    const { collectionId, format } = args;

    if (!collectionId) {
      throw new Error("collectionId parameter is required");
    }

    const params: Record<string, unknown> = {};
    if (format) {
      params.format = format;
    }

    const response = await this.client.get(
      `/collections/${collectionId}/schema`,
      { params }
    );
    return response.data;
  }

  private async getCollectionItems(
    args: Record<string, unknown>
  ): Promise<unknown> {
    const { collectionId } = args;

    if (!collectionId) {
      throw new Error("collectionId parameter is required");
    }

    const response = await this.client.get(
      `/collections/${collectionId}/items`
    );
    return response.data;
  }

  private async addCollectionItems(
    args: Record<string, unknown>
  ): Promise<unknown> {
    const { collectionId, items } = args;

    if (!collectionId || !items) {
      throw new Error("collectionId and items parameters are required");
    }

    const response = await this.client.post(
      `/collections/${collectionId}/items`,
      { items }
    );
    return response.data;
  }

  private async deleteCollectionItems(
    args: Record<string, unknown>
  ): Promise<unknown> {
    const { collectionId, idsToDelete } = args;

    if (!collectionId || !idsToDelete) {
      throw new Error("collectionId and idsToDelete parameters are required");
    }

    const response = await this.client.delete(
      `/collections/${collectionId}/items`,
      { data: { idsToDelete } }
    );
    return response.data;
  }

  private async updateCollectionItems(
    args: Record<string, unknown>
  ): Promise<unknown> {
    const { collectionId, itemsToUpdate } = args;

    if (!collectionId || !itemsToUpdate) {
      throw new Error("collectionId and itemsToUpdate parameters are required");
    }

    const response = await this.client.put(
      `/collections/${collectionId}/items`,
      { itemsToUpdate }
    );
    return response.data;
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("Craft API MCP Server running on stdio");
  }
}

const server = new CraftAPIServer();
server.run().catch(console.error);
