# ChatGPT App Integration with Smithery

Make Bl1nk Architect available as a ChatGPT App using Smithery MCP.

## Quick Setup (5 minutes)

### Prerequisites

- Node.js 18+
- Smithery API key (free at smithery.ai/account/api-keys)
- Python 3.11+ (for bot server)

### 1. Create Smithery App

```bash
npx create-smithery@latest bl1nk-chatgpt --gpt
cd bl1nk-chatgpt
```

### 2. Project Structure

```
bl1nk-chatgpt/
├── app/
│   ├── server/
│   │   └── index.ts        # MCP server (defines tools)
│   ├── shared/
│   │   └── types.ts        # Shared TypeScript types
│   └── web/
│       └── src/
│           └── widget.tsx  # React widget
├── smithery.yaml           # Config
└── package.json
```

### 3. Server Code (app/server/index.ts)

```typescript
import { widget } from "@smithery/sdk";

export default widget.server().tool({
  name: "analyze_repository",
  description: "Analyze GitHub repository with Bl1nk Architect",
  input: {
    type: "object",
    properties: {
      repository_url: {
        type: "string",
        description: "GitHub repository URL"
      },
      analysis_type: {
        type: "string",
        enum: ["quick", "full", "security"],
        description: "Type of analysis"
      }
    },
    required: ["repository_url"]
  },
  async execute(input) {
    // Call your Bl1nk Architect bot here
    const response = await fetch("YOUR_BOT_URL", {
      method: "POST",
      headers: {
        "Authorization": "Bearer YOUR_KEY",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        type: "query",
        query: [
          {
            role: "user",
            content: `Analyze: ${input.repository_url} (${input.analysis_type})`
          }
        ]
      })
    });

    const data = await response.json();
    
    return {
      structuredData: {
        repository: input.repository_url,
        analysis_type: input.analysis_type,
        result: data.analysis,
        status: "completed"
      }
    };
  }
});
```

### 4. Shared Types (app/shared/types.ts)

```typescript
export interface AnalysisRequest {
  repository_url: string;
  analysis_type: "quick" | "full" | "security";
}

export interface AnalysisResult {
  repository: string;
  analysis_type: string;
  result: string;
  status: "completed" | "error";
}
```

### 5. Widget Code (app/web/src/widget.tsx)

```typescript
import React from "react";
import { useToolOutput, useTheme } from "@smithery/sdk/react";
import type { AnalysisResult } from "../../shared/types";

export default function AnalysisWidget() {
  const { isDark } = useTheme();
  const data = useToolOutput<AnalysisResult>();

  if (!data) {
    return <div>Loading analysis...</div>;
  }

  return (
    <div style={{
      padding: "20px",
      background: isDark ? "#1f2937" : "#f3f4f6",
      borderRadius: "8px"
    }}>
      <h2>Analysis Results</h2>
      <p><strong>Repository:</strong> {data.repository}</p>
      <p><strong>Type:</strong> {data.analysis_type}</p>
      <pre>{data.result}</pre>
    </div>
  );
}
```

### 6. Configuration (smithery.yaml)

```yaml
name: "Bl1nk Architect"
description: "GitHub repository architecture analyzer"
version: "1.0.0"

tools:
  - name: analyze_repository
    description: "Analyze repository architecture"

widget:
  title: "Architecture Analysis"
  theme: dark
```

### 7. Run Development Server

```bash
npm run dev
```

### 8. Deploy to Smithery

```bash
npm run deploy
```

## Integration Steps

### Step 1: Configure Bot Connection

In `app/server/index.ts`, set your Bl1nk Architect bot URL:

```typescript
const BOT_URL = process.env.BL1NK_BOT_URL;
const BOT_KEY = process.env.BL1NK_BOT_KEY;
```

### Step 2: Add Environment Variables

Create `.env`:

```
BL1NK_BOT_URL=https://your-modal-url.modal.run
BL1NK_BOT_KEY=your_poe_access_key
```

### Step 3: Implement Tool Handlers

Map ChatGPT prompts to Bl1nk bot queries:

```typescript
const queryMap = {
  "analyze architecture": "Analyze my repository",
  "check dependencies": "Check my dependencies",
  "find duplicates": "Find code duplicates",
  "create plan": "Create refactoring plan"
};
```

### Step 4: Parse Streaming Response

Handle SSE responses from bot:

```typescript
async function streamAnalysis(query) {
  const response = await fetch(BOT_URL, {
    method: "POST",
    body: JSON.stringify({
      type: "query",
      query: [{ role: "user", content: query }]
    })
  });

  for await (const event of response.body) {
    if (event.type === "text") {
      yield event.data.text;
    }
  }
}
```

## Features Available

### Input Options

```typescript
tool({
  input: {
    type: "object",
    properties: {
      repository_url: { type: "string" },
      analysis_type: { enum: ["quick", "full"] },
      format: { enum: ["markdown", "json"] }
    }
  }
})
```

### Widget Display

```typescript
// Theme support
const { isDark } = useTheme();

// Data access
const data = useToolOutput<YourType>();

// Loading states
if (!data) return <Loading />;
```

### Real-time Updates

```typescript
// Stream responses as they come in
async function* streamUpdates() {
  yield { status: "analyzing" };
  yield { status: "scanning", progress: 25 };
  yield { status: "completed", result: data };
}
```

## Testing Locally

```bash
npm run dev

# Test in ChatGPT:
# "Analyze my repository on GitHub"
# "Check code quality of myrepo"
# "Find duplicates in my-project"
```

## Deployment

### To Smithery

```bash
npm run build
npm run deploy
```

### To OpenAI Apps

1. Build: `npm run build`
2. Package: `npm run package`
3. Upload to OpenAI Apps
4. Configure in ChatGPT

## Environment Setup

Create `smithery.yaml`:

```yaml
name: "Bl1nk Architect"
description: "AI-powered GitHub architecture analyzer"

functions:
  - name: analyze_repository
    description: "Analyze GitHub repository structure"
    parameters:
      type: object
      properties:
        url:
          type: string
          description: "Repository URL"

widget:
  title: "Analysis Results"
  height: 400
```

## Best Practices

1. **Type Safety**: Use shared types in `app/shared/`
2. **Error Handling**: Catch and display errors gracefully
3. **Streaming**: Handle long-running analyses with progress
4. **Caching**: Cache results to avoid repeated calls
5. **Validation**: Validate input URLs before processing

## Troubleshooting

**Widget not showing?**
- Check `smithery.yaml` is valid
- Verify `structuredData` structure matches types
- Check console for errors

**Bot connection failing?**
- Verify BOT_URL is accessible
- Check authorization token
- Test endpoint with curl

**Slow analysis?**
- Implement streaming for long tasks
- Add progress indicators
- Consider caching results

## Next Steps

- [ ] Setup Smithery project
- [ ] Configure bot connection
- [ ] Implement tool handlers
- [ ] Test locally
- [ ] Deploy to Smithery
- [ ] Add to ChatGPT

