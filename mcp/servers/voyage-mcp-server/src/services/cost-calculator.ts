export class CostCalculator {
  private embeddingCostPerMillion: Record<string, number>;
  private rerankCostPerThousand: Record<string, number>;
  private provider: string;
  private minTokensForRerank: number;

  constructor(
    embeddingCostPerMillion: Record<string, number>,
    rerankCostPerThousand: Record<string, number>,
    provider: string,
    minTokensForRerank: number = 100
  ) {
    this.embeddingCostPerMillion = embeddingCostPerMillion;
    this.rerankCostPerThousand = rerankCostPerThousand;
    this.provider = provider;
    this.minTokensForRerank = minTokensForRerank;
  }

  estimateTokens(text: string): number {
    // Rough estimation: 1 token ≈ 4 characters
    return Math.ceil(text.length / 4);
  }

  calculateEmbeddingCost(tokens: number): number {
    const costPerMillion = this.embeddingCostPerMillion[this.provider] || 0.10;
    return (tokens / 1000000) * costPerMillion;
  }

  calculateRerankCost(tokens: number): number {
    const costPerThousand = this.rerankCostPerThousand[this.provider] || 1.00;
    return (tokens / 1000) * costPerThousand;
  }

  getLLMCostEstimate(query: string): number {
    // Rough estimation for LLM cost
    const tokens = this.estimateTokens(query);
    // Assuming LLM costs about 10x more than embedding
    return (tokens / 1000000) * 0.001;
  }

  getMinTokensForRerank(): number {
    return this.minTokensForRerank;
  }

  updateProvider(provider: string): void {
    this.provider = provider;
  }
}
