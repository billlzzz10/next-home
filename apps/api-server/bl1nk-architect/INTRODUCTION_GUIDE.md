# Introduction Message Support

Bl1nk Architect includes professional introduction messages for onboarding.

## What It Does

Introduction messages are shown to users when they first interact with your bot.

Features:
- Friendly welcome message
- Feature overview
- Getting started instructions
- Customizable per user state
- Multiple pre-defined messages

## Implementation

The introduction message is set in bot settings:

```python
from src.introduction_manager import IntroductionMessages

async def get_settings(self, setting):
    return fp.SettingsResponse(
        introduction_message=IntroductionMessages.MAIN,
        allow_attachments=True
    )
```

## Available Messages

**IntroductionMessages.MAIN** - Default welcome
**IntroductionMessages.AUTHENTICATED** - After GitHub auth
**IntroductionMessages.HELP_MESSAGE** - Detailed help
**IntroductionMessages.WAITING_AUTH** - Auth needed
**IntroductionMessages.ANALYSIS_MODE** - During analysis

## Customization

Edit in src/introduction_manager.py:

```python
def get_introduction_message() -> str:
    return """Your custom message"""
```

Add to IntroductionMessages class:

```python
class IntroductionMessages:
    CUSTOM = """Your message"""
```

Use in get_settings:

```python
introduction_message=IntroductionMessages.CUSTOM
```

## Usage Examples

### Dynamic Selection

```python
if is_authenticated(user_id):
    msg = IntroductionMessages.AUTHENTICATED
else:
    msg = IntroductionMessages.MAIN
```

### Personalization

```python
from src.introduction_manager import IntroductionManager

intro = IntroductionManager.get_custom_introduction(
    repo_name="my-repo",
    user_name="John"
)
```

## Best Practices

- Keep under 500 characters
- Use clear sections with headers
- Include bullet points
- Add emojis for visual appeal
- Include call-to-action
- Use Markdown formatting
- Test before deploy

## Testing

```bash
curl -X POST http://localhost:8000 \
  -H "Authorization: Bearer KEY" \
  -d '{"type":"settings"}'
```

## Deployment

After updating:

1. Commit changes
2. Push to GitHub
3. GitHub Actions deploys
4. New users see updated message
5. Changes take effect immediately

## Files

- src/introduction_manager.py - Message definitions
- INTRODUCTION_GUIDE.md - This guide

