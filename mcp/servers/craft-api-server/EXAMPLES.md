# Craft API MCP Server - Usage Examples

## Common Use Cases

### 1. List All Documents

Get an overview of all accessible documents.

```json
{
  "tool": "list_documents"
}
```

**Response:**
```json
{
  "items": [
    {
      "id": "doc-abc123",
      "title": "Project Documentation",
      "isDeleted": false
    },
    {
      "id": "doc-def456",
      "title": "Team Notes",
      "isDeleted": false
    }
  ]
}
```

### 2. Get Document Content

Retrieve a complete document structure.

```json
{
  "tool": "get_blocks",
  "arguments": {
    "id": "doc-abc123",
    "maxDepth": -1,
    "fetchMetadata": true
  }
}
```

### 3. Add New Content to Document

Create a new section with markdown content.

```json
{
  "tool": "insert_blocks",
  "arguments": {
    "markdown": "## Meeting Notes\n\n### Attendees\n- Alice\n- Bob\n\n### Key Points\n1. Project deadline: January 15\n2. Budget approved: $50k",
    "position": {
      "position": "end",
      "pageId": "doc-abc123"
    }
  }
}
```

### 4. Search Within a Document

Find content using regular expressions.

```json
{
  "tool": "search_document",
  "arguments": {
    "documentId": "doc-abc123",
    "pattern": "deadline|urgent",
    "caseSensitive": false,
    "beforeBlockCount": 1,
    "afterBlockCount": 1
  }
}
```

### 5. Search Across All Documents

Find matching content with relevance ranking.

```json
{
  "tool": "search_documents",
  "arguments": {
    "include": "project milestone"
  }
}
```

### 6. Update Document Content

Modify existing block content.

```json
{
  "tool": "update_blocks",
  "arguments": {
    "blocks": [
      {
        "id": "block-123",
        "markdown": "## Updated Meeting Notes\n\n### New Information\n- Budget increased to $75k\n- Deadline extended to February 1"
      }
    ]
  }
}
```

### 7. Create Structured Content

Add blocks with specific formatting.

```json
{
  "tool": "insert_blocks",
  "arguments": {
    "blocks": [
      {
        "type": "text",
        "markdown": "## Project Overview",
        "textStyle": "h2"
      },
      {
        "type": "text",
        "markdown": "This section contains important project information.",
        "textStyle": "body"
      }
    ],
    "position": {
      "position": "start",
      "pageId": "doc-abc123"
    }
  }
}
```

### 8. Move Content Between Sections

Reorder or move blocks.

```json
{
  "tool": "move_blocks",
  "arguments": {
    "blockIds": ["block-123", "block-124"],
    "position": {
      "position": "end",
      "pageId": "doc-def456"
    }
  }
}
```

### 9. Work with Collections

List all available collections.

```json
{
  "tool": "list_collections"
}
```

### 10. Add Items to a Collection

Insert new items with metadata.

```json
{
  "tool": "add_collection_items",
  "arguments": {
    "collectionId": "col-tasks",
    "items": [
      {
        "title": "Complete API documentation",
        "properties": {
          "status": "in-progress",
          "assignee": "Alice",
          "dueDate": "2024-01-15"
        }
      },
      {
        "title": "Review code changes",
        "properties": {
          "status": "pending",
          "assignee": "Bob",
          "dueDate": "2024-01-12"
        }
      }
    ]
  }
}
```

### 11. Get Collection Schema

Understand collection structure.

```json
{
  "tool": "get_collection_schema",
  "arguments": {
    "collectionId": "col-tasks",
    "format": "json-schema-items"
  }
}
```

### 12. Retrieve Collection Items

Get all items from a collection.

```json
{
  "tool": "get_collection_items",
  "arguments": {
    "collectionId": "col-tasks"
  }
}
```

### 13. Update Collection Items

Modify existing collection items.

```json
{
  "tool": "update_collection_items",
  "arguments": {
    "collectionId": "col-tasks",
    "itemsToUpdate": [
      {
        "id": "item-001",
        "title": "Complete API documentation",
        "properties": {
          "status": "completed",
          "completedDate": "2024-01-10"
        }
      }
    ]
  }
}
```

### 14. Delete Content

Remove blocks from documents.

```json
{
  "tool": "delete_blocks",
  "arguments": {
    "blockIds": ["block-outdated", "block-duplicate"]
  }
}
```

### 15. Delete Collection Items

Remove items from a collection.

```json
{
  "tool": "delete_collection_items",
  "arguments": {
    "collectionId": "col-tasks",
    "idsToDelete": ["item-archived-001", "item-archived-002"]
  }
}
```

## Advanced Workflows

### Workflow 1: Knowledge Base Update

1. Search for outdated content
2. Update relevant blocks
3. Add new information
4. Reorganize sections

```json
[
  {
    "tool": "search_documents",
    "arguments": { "include": "deprecated" }
  },
  {
    "tool": "update_blocks",
    "arguments": {
      "blocks": [
        { "id": "deprecated-block", "markdown": "## Updated Information\n..." }
      ]
    }
  },
  {
    "tool": "insert_blocks",
    "arguments": {
      "markdown": "## New Features\n...",
      "position": { "position": "end", "pageId": "doc-123" }
    }
  }
]
```

### Workflow 2: Task Management

1. List all collections
2. Get collection items
3. Update status
4. Add new tasks

```json
[
  { "tool": "list_collections" },
  { "tool": "get_collection_items", "arguments": { "collectionId": "col-tasks" } },
  {
    "tool": "update_collection_items",
    "arguments": {
      "collectionId": "col-tasks",
      "itemsToUpdate": [
        { "id": "task-1", "properties": { "status": "completed" } }
      ]
    }
  },
  {
    "tool": "add_collection_items",
    "arguments": {
      "collectionId": "col-tasks",
      "items": [
        { "title": "New Task", "properties": { "status": "pending" } }
      ]
    }
  }
]
```

### Workflow 3: Content Migration

1. Get source document
2. Parse content (in your application)
3. Insert into target document
4. Verify migration

```json
[
  { "tool": "get_blocks", "arguments": { "id": "source-doc" } },
  {
    "tool": "insert_blocks",
    "arguments": {
      "markdown": "migrated-content-here",
      "position": { "position": "end", "pageId": "target-doc" }
    }
  }
]
```

## Error Handling Examples

### Missing Required Parameter

```json
{
  "tool": "get_blocks"
}
```

Response:
```json
{
  "error": "Error: id parameter is required"
}
```

### Invalid Document ID

```json
{
  "tool": "get_blocks",
  "arguments": { "id": "invalid-doc" }
}
```

Response:
```json
{
  "error": "Error: 404 Not Found"
}
```

### Timeout on Large Document

```json
{
  "tool": "get_blocks",
  "arguments": {
    "id": "very-large-doc",
    "maxDepth": -1
  }
}
```

Potential Response:
```json
{
  "error": "Error: timeout of 30000ms exceeded"
}
```

Solution: Use `maxDepth` to limit the scope:
```json
{
  "tool": "get_blocks",
  "arguments": {
    "id": "very-large-doc",
    "maxDepth": 2
  }
}
```

## Tips & Best Practices

### 1. Always List Documents First

Get available document IDs before other operations:
```json
{ "tool": "list_documents" }
```

### 2. Use Reasonable maxDepth Values

- `-1`: All descendants (can be slow for large documents)
- `1-2`: Usually sufficient for most use cases
- `0`: Only the specified block

### 3. Search Before Update

Always verify content before updating:
```json
[
  {
    "tool": "search_documents",
    "arguments": { "include": "search-term" }
  },
  {
    "tool": "update_blocks",
    "arguments": { "blocks": [...] }
  }
]
```

### 4. Batch Operations Efficiently

Group similar operations together to reduce latency.

### 5. Use Collections for Structured Data

Collections are ideal for:
- Task lists
- Databases
- Catalogs
- Structured records

### 6. Test with Non-Critical Data

Always test delete/update operations with test content first.

### 7. Handle Nested Content Carefully

When working with deeply nested blocks, fetch gradually:
```json
{
  "tool": "get_blocks",
  "arguments": {
    "id": "block-parent",
    "maxDepth": 1
  }
}
```

Then fetch children as needed.

---

For more information, refer to README.md and the Craft API documentation.
