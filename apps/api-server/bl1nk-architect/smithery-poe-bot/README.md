# Bl1nk Architect - Smithery Poe Chat Bot

ใช้ Bl1nk Architect ผ่าน Poe โดยตรงผ่าน Smithery MCP

## วิธีการใช้งาน

### 1. Create Smithery Poe Bot

```bash
npx create-smithery@latest bl1nk-poe-bot --template poe
cd bl1nk-poe-bot
```

### 2. Configure Bot (smithery.yaml)

```yaml
name: Bl1nk Architect
description: GitHub repository architecture analyzer

bot:
  introduction_message: |
    🏗️ Bl1nk Architect
    
    I analyze GitHub repositories.
    
    Try: "Analyze my repo"
```

### 3. Implementation (src/index.ts)

```typescript
import { PoeBot } from '@smithery/poe-sdk';

export const bot = new PoeBot({
  async onMessage(message, context) {
    // Call Bl1nk backend
    const response = await fetch(
      process.env.BLINK_BOT_URL,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.POE_KEY}`,
        },
        body: JSON.stringify({
          type: 'query',
          query: [{
            role: 'user',
            content: message.content
          }],
          user_id: context.user_id,
          conversation_id: context.conversation_id,
        })
      }
    );

    // Stream response
    const reader = response.body.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const text = new TextDecoder().decode(value);
      await context.send_message(text);
    }
  }
});
```

### 4. Deploy

```bash
npm install
npm run build
smithery deploy
```

### 5. Register on Poe

Go to poe.com/create_bot?server=1:
- Server URL: Your Smithery URL
- Access Key: POE_ACCESS_KEY

### 6. Chat!

Find your bot on Poe.com and start chatting

## Features

✅ Real-time chat
✅ Streaming
✅ File attachments
✅ Error handling
✅ Auto retry

## Environment

```bash
export BLINK_BOT_URL=http://localhost:8000
export POE_KEY=your_key
export POE_ACCESS_KEY=your_access_key
```

## Test Locally

```bash
npm run dev
```

## Cost

Free tier:
- 10,000 messages/month
- Unlimited deployments

