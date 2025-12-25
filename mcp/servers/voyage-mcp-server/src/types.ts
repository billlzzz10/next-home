import { z } from 'zod';

// ==================== Log Types ====================
export const LogEntrySchema = z.object({
  timestamp: z.string().datetime(),
  userId: z.string(),
  type: z.enum(['search_request', 'search_result', 'document_import', 'error', 'system']),
  method: z.string().optional(),
  params: z.any().optional(),
  result: z.any().optional(),
  error: z.string().optional(),
  stack: z.string().optional(),
  costEstimate: z.number().optional(),
  tokens: z.number().optional(),
  metadata: z.record(z.any()).optional()
});

export type LogEntry = z.infer<typeof LogEntrySchema>;

// ==================== Search Types ====================
export const SearchResultSchema = z.object({
  id: z.string(),
  score: z.number(),
  content: z.string(),
  metadata: z.record(z.any()).optional(),
  source: z.string().optional(),
  tokens: z.number().optional()
});

export type SearchResult = z.infer<typeof SearchResultSchema>;

export const SearchResponseSchema = z.object({
  results: z.array(SearchResultSchema),
  total: z.number(),
  costEstimate: z.number(),
  tokensUsed: z.number(),
  shouldUseLLM: z.boolean(),
  rerankUsed: z.boolean(),
  provider: z.string()
});

export type SearchResponse = z.infer<typeof SearchResponseSchema>;

// ==================== Document Types ====================
export const DocumentSchema = z.object({
  id: z.string(),
  content: z.string(),
  title: z.string().optional(),
  source: z.string().optional(),
  metadata: z.record(z.any()).optional(),
  createdAt: z.string().datetime().optional(),
  updatedAt: z.string().datetime().optional()
});

export type Document = z.infer<typeof DocumentSchema>;

// ==================== Config Types ====================
export const ConfigSchema = z.object({
  qdrant: z.object({
    url: z.string().default('http://localhost:6333'),
    apiKey: z.string().optional(),
    collectionName: z.string().default('mcp-knowledge-base'),
    vectorSize: z.number().default(1024),
    recreateCollection: z.boolean().default(false)
  }),
  providers: z.object({
    primary: z.enum(['voyage', 'mistral']).default('voyage'),
    voyage: z.object({
      apiKey: z.string().optional(),
      embeddingModel: z.string().default('voyage-large-2'),
      rerankModel: z.string().default('voyage-rerank-lite-1')
    }),
    mistral: z.object({
      apiKey: z.string().optional(),
      embeddingModel: z.string().default('mistral-embed')
    })
  }),
  logging: z.object({
    enabled: z.boolean().default(true),
    baseLogDir: z.string().default('user_logs'),
    rotateDays: z.number().default(30),
    logSearchQueries: z.boolean().default(true),
    logCostEstimates: z.boolean().default(true)
  }),
  cost: z.object({
    threshold: z.number().default(0.05),
    embeddingCostPerMillion: z.object({
      voyage: z.number().default(0.10),
      mistral: z.number().default(0.15)
    }),
    rerankCostPerThousand: z.object({
      voyage: z.number().default(1.00),
      mistral: z.number().default(0.80)
    })
  }),
  search: z.object({
    topK: z.number().default(5),
    scoreThreshold: z.number().default(0.82),
    batchSize: z.number().default(10),
    useRerank: z.boolean().default(true),
    minTokensForRerank: z.number().default(100)
  }),
  filters: z.object({
    default: z.object({
      minScore: z.number().default(0.7),
      maxAgeDays: z.number().optional(),
      requiredTags: z.array(z.string()).default([])
    }),
    payload: z.record(z.any()).default({})
  }),
  system: z.object({
    userIdHeader: z.string().default('X-User-ID'),
    enableCostEstimation: z.boolean().default(true),
    autoSaveNewQAPairs: z.boolean().default(true)
  })
});

export type AppConfig = z.infer<typeof ConfigSchema>;
