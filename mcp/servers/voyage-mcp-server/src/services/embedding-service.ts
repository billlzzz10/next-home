import axios from 'axios';
import { CostCalculator } from './cost-calculator.js';

export interface EmbeddingServiceConfig {
  voyageApiKey?: string;
  mistralApiKey?: string;
}

export interface EmbeddingResult {
  embedding: number[];
  tokens: number;
}

export interface RerankResult {
  results: Array<{
    id: string;
    score: number;
    content: string;
  }>;
  tokens: number;
}

export class EmbeddingService {
  private provider: string;
  private voyageApiKey?: string;
  private mistralApiKey?: string;
  private costCalculator: CostCalculator | null = null;

  constructor(
    provider: string = 'voyage',
    config: EmbeddingServiceConfig = {}
  ) {
    this.provider = provider;
    this.voyageApiKey = config.voyageApiKey;
    this.mistralApiKey = config.mistralApiKey;
  }

  async createEmbedding(text: string): Promise<EmbeddingResult> {
    if (this.provider === 'voyage') {
      return this.createVoyageEmbedding(text);
    } else if (this.provider === 'mistral') {
      return this.createMistralEmbedding(text);
    } else {
      throw new Error(`Unknown provider: ${this.provider}`);
    }
  }

  private async createVoyageEmbedding(text: string): Promise<EmbeddingResult> {
    if (!this.voyageApiKey) {
      throw new Error('Voyage API key is not configured');
    }

    try {
      const response = await axios.post(
        'https://api.voyageai.com/v1/embeddings',
        {
          input: text,
          model: 'voyage-large-2'
        },
        {
          headers: {
            'Authorization': `Bearer ${this.voyageApiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );

      const embedding = response.data.data[0].embedding;
      const tokens = response.data.usage.total_tokens;

      return { embedding, tokens };
    } catch (error: any) {
      throw new Error(`Voyage API error: ${error.message}`);
    }
  }

  private async createMistralEmbedding(text: string): Promise<EmbeddingResult> {
    if (!this.mistralApiKey) {
      throw new Error('Mistral API key is not configured');
    }

    try {
      const response = await axios.post(
        'https://api.mistral.ai/v1/embeddings',
        {
          model: 'mistral-embed',
          input: text
        },
        {
          headers: {
            'Authorization': `Bearer ${this.mistralApiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );

      const embedding = response.data.data[0].embedding;
      const tokens = response.data.usage.prompt_tokens;

      return { embedding, tokens };
    } catch (error: any) {
      throw new Error(`Mistral API error: ${error.message}`);
    }
  }

  async rerank(
    query: string,
    documents: string[]
  ): Promise<RerankResult> {
    if (this.provider === 'voyage') {
      return this.rerankVoyage(query, documents);
    } else if (this.provider === 'mistral') {
      return this.rerankMistral(query, documents);
    } else {
      throw new Error(`Unknown provider: ${this.provider}`);
    }
  }

  private async rerankVoyage(
    query: string,
    documents: string[]
  ): Promise<RerankResult> {
    if (!this.voyageApiKey) {
      throw new Error('Voyage API key is not configured');
    }

    try {
      const response = await axios.post(
        'https://api.voyageai.com/v1/rerank',
        {
          query,
          documents,
          model: 'voyage-rerank-lite-1',
          top_k: documents.length
        },
        {
          headers: {
            'Authorization': `Bearer ${this.voyageApiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );

      const results = response.data.results.map((item: any, idx: number) => ({
        id: `doc_${item.index}`,
        score: item.relevance_score,
        content: documents[item.index]
      }));

      return {
        results,
        tokens: Math.ceil(query.length / 4) // Rough estimation
      };
    } catch (error: any) {
      throw new Error(`Voyage Rerank API error: ${error.message}`);
    }
  }

  private async rerankMistral(
    query: string,
    documents: string[]
  ): Promise<RerankResult> {
    // Mistral doesn't have native rerank, so we return basic ranking
    const results = documents.map((doc, idx) => ({
      id: `doc_${idx}`,
      score: 0.5,
      content: doc
    }));

    return {
      results,
      tokens: Math.ceil((query.length + documents.join('').length) / 4)
    };
  }

  getProvider(): string {
    return this.provider;
  }

  updateProvider(provider: string, config: EmbeddingServiceConfig): void {
    this.provider = provider;
    this.voyageApiKey = config.voyageApiKey;
    this.mistralApiKey = config.mistralApiKey;
  }

  setCostCalculator(calculator: CostCalculator): void {
    this.costCalculator = calculator;
  }
}
