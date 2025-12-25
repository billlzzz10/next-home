export interface FilterOptions {
  minScore?: number;
  maxAgeDays?: number;
  requiredTags?: string[];
  categories?: string[];
  sources?: string[];
  priority?: number;
  minReadability?: number;
  dateRange?: {
    start?: string;
    end?: string;
  };
  wordCount?: {
    min?: number;
    max?: number;
  };
  customFilters?: {
    field: string;
    value: any;
    operator: 'equals' | 'contains' | 'gte' | 'lte';
  }[];
}

export function buildPayloadFilter(filters: FilterOptions): any | undefined {
  if (!filters || Object.keys(filters).length === 0) {
    return undefined;
  }

  const conditions: any[] = [];

  if (filters.minScore !== undefined) {
    conditions.push({
      key: 'score',
      range: {
        gte: filters.minScore
      }
    });
  }

  if (filters.dateRange) {
    const range: any = {};

    if (filters.dateRange.start) {
      range.gte = new Date(filters.dateRange.start).toISOString();
    }

    if (filters.dateRange.end) {
      range.lte = new Date(filters.dateRange.end).toISOString();
    }

    if (Object.keys(range).length > 0) {
      conditions.push({
        key: 'metadata.lastUpdated',
        range
      });
    }
  }

  if (filters.requiredTags && filters.requiredTags.length > 0) {
    for (const tag of filters.requiredTags) {
      conditions.push({
        key: 'metadata.tags',
        match: { value: tag }
      });
    }
  }

  if (filters.categories && filters.categories.length > 0) {
    conditions.push({
      key: 'metadata.category',
      match: {
        value: {
          $in: filters.categories
        }
      }
    });
  }

  if (filters.sources && filters.sources.length > 0) {
    conditions.push({
      key: 'metadata.source',
      match: {
        value: {
          $in: filters.sources
        }
      }
    });
  }

  if (filters.priority !== undefined) {
    conditions.push({
      key: 'metadata.priority',
      range: {
        gte: filters.priority
      }
    });
  }

  if (filters.minReadability !== undefined) {
    conditions.push({
      key: 'metadata.readability',
      range: {
        gte: filters.minReadability
      }
    });
  }

  if (filters.wordCount) {
    const range: any = {};

    if (filters.wordCount.min !== undefined) {
      range.gte = filters.wordCount.min;
    }

    if (filters.wordCount.max !== undefined) {
      range.lte = filters.wordCount.max;
    }

    if (Object.keys(range).length > 0) {
      conditions.push({
        key: 'metadata.wordCount',
        range
      });
    }
  }

  if (filters.customFilters) {
    for (const filter of filters.customFilters) {
      switch (filter.operator) {
        case 'equals':
          conditions.push({
            key: filter.field,
            match: { value: filter.value }
          });
          break;
        case 'contains':
          conditions.push({
            key: filter.field,
            match: { value: filter.value }
          });
          break;
        case 'gte':
          conditions.push({
            key: filter.field,
            range: { gte: filter.value }
          });
          break;
        case 'lte':
          conditions.push({
            key: filter.field,
            range: { lte: filter.value }
          });
          break;
      }
    }
  }

  if (filters.maxAgeDays !== undefined) {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - filters.maxAgeDays);

    conditions.push({
      key: 'metadata.lastUpdated',
      range: {
        gte: cutoffDate.toISOString()
      }
    });
  }

  if (conditions.length === 0) {
    return undefined;
  }

  return {
    must: conditions
  };
}
