import { QdrantClient } from '@qdrant/js-client-rest';
import { Document } from '../types.js';

export class QdrantVectorStore {
  private client: QdrantClient;
  private collectionName: string;
  private vectorSize: number;

  constructor(url: string, apiKey?: string, collectionName: string = 'mcp-knowledge-base') {
    this.client = new QdrantClient({
      url,
      apiKey
    });
    this.collectionName = collectionName;
    this.vectorSize = 1024;
  }

  async initialize(vectorSize: number, recreate: boolean = false): Promise<void> {
    this.vectorSize = vectorSize;

    try {
      const collections = await this.client.getCollections();

      const exists = collections.collections.some(c => c.name === this.collectionName);

      if (exists && recreate) {
        await this.client.deleteCollection(this.collectionName);
      }

      if (!exists || recreate) {
        await this.client.createCollection(this.collectionName, {
          vectors: {
            size: vectorSize,
            distance: 'Cosine'
          }
        });
      }
    } catch (error) {
      throw new Error(`Failed to initialize Qdrant collection: ${error}`);
    }
  }

  async addDocument(doc: Document, vector: number[]): Promise<void> {
    try {
      await this.client.upsert(this.collectionName, {
        points: [
          {
            id: doc.id,
            vector: vector,
            payload: {
              content: doc.content,
              title: doc.title,
              source: doc.source,
              metadata: doc.metadata,
              createdAt: doc.createdAt,
              updatedAt: doc.updatedAt
            }
          }
        ]
      });
    } catch (error) {
      throw new Error(`Failed to add document: ${error}`);
    }
  }

  async search(vector: number[], topK: number, filter?: any): Promise<any[]> {
    try {
      const results = await this.client.search(this.collectionName, {
        vector: vector,
        limit: topK,
        query_filter: filter
      });

      return results.map(r => ({
        id: r.id,
        score: r.score,
        content: r.payload?.content,
        metadata: r.payload?.metadata
      }));
    } catch (error) {
      throw new Error(`Failed to search: ${error}`);
    }
  }

  async deleteDocument(docId: string): Promise<void> {
    try {
      await this.client.delete(this.collectionName, {
        points_selector: {
          points: [docId]
        }
      });
    } catch (error) {
      throw new Error(`Failed to delete document: ${error}`);
    }
  }

  getCollectionName(): string {
    return this.collectionName;
  }

  updateConnection(url: string, apiKey?: string): void {
    this.client = new QdrantClient({
      url,
      apiKey
    });
  }
}
