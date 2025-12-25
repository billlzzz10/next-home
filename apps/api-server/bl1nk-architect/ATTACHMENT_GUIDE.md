# File Attachment Support Guide

Bl1nk Architect now supports sending files (attachments) with bot responses.

## Overview

The bot can send files to users in multiple formats:
- **Markdown Reports** (.md) - Architecture analysis reports
- **JSON Files** (.json) - Structured analysis data
- **CSV Files** (.csv) - Task lists and summaries
- **Text Files** (.txt) - Raw output

## Architecture

### AttachmentHandler (`src/attachment_handler.py`)

Handles file preparation and validation:

```python
from src.attachment_handler import AttachmentHandler

handler = AttachmentHandler()

# Prepare markdown file
file_bytes, filename = await handler.prepare_markdown_file(
    content="# My Report\n...",
    filename="report.md"
)

# Prepare JSON file
file_bytes, filename = await handler.prepare_json_file(
    data={"key": "value"},
    filename="data.json"
)

# Prepare CSV file
file_bytes, filename = await handler.prepare_csv_file(
    headers=["Task", "Priority"],
    rows=[["Fix bugs", "High"]],
    filename="tasks.csv"
)
```

## Usage in Bot Response

### Example 1: Send Architecture Report

```python
async def get_response(self, request: fp.QueryRequest):
    yield fp.MetaResponse(content_type="text/markdown")
    
    # Generate report
    report = "# Architecture Analysis\n\n..."
    
    # Send report as attachment
    from src.attachment_handler import AttachmentHandler
    handler = AttachmentHandler()
    
    file_bytes, filename = await handler.prepare_markdown_file(
        report,
        "analysis.md"
    )
    
    # First, send text response
    yield fp.PartialResponse(text="Analysis complete! Report attached.")
    
    # Then send file (using post_message_attachment in fastapi_poe)
    # await self.post_message_attachment(
    #     message_id=request.message_id,
    #     file_data=file_bytes,
    #     filename=filename
    # )
    
    yield fp.PartialResponse(text="\nDownload the attached report for details.")
```

### Example 2: Send Task Summary

```python
async def send_task_summary(self, tasks):
    from src.attachment_handler import AttachmentHandler
    handler = AttachmentHandler()
    
    # Create CSV
    headers = ["Task ID", "Description", "Priority", "Status"]
    rows = [
        ["1", "Fix dependencies", "High", "Pending"],
        ["2", "Add tests", "Medium", "Pending"],
    ]
    
    file_bytes, filename = await handler.prepare_csv_file(
        headers, rows, "tasks.csv"
    )
    
    # Send to user
    return file_bytes, filename
```

## File Limits

- **Maximum file size**: 50 MB (configurable)
- **Maximum files per response**: 20
- **Supported formats**: Any, but optimized for:
  - Text (.txt, .md)
  - Data (.json, .csv)
  - Documents (.pdf)
  - Images (.png, .jpg, .gif)

## Integration with Poe API

When using `fastapi_poe` library, send attachments via `post_message_attachment`:

```python
await self.post_message_attachment(
    message_id=request.message_id,
    file_data=file_bytes,
    filename="report.md",
    content_type="text/markdown"
)
```

**Important**: This must be called during `get_response` for the current request being handled.

## Workflow Integration

Orchestrator can generate reports with attachments:

1. **Run analysis** (Steps 1-8)
2. **Generate report** (markdown/JSON/CSV)
3. **Attach file** to bot response
4. **Stream text** with link to download

## Examples

### Generate Complete Report

```python
from src.orchestrator_with_attachments import create_architecture_report

file_bytes, filename, content_type = await create_architecture_report(
    repo_name="my-repo",
    analysis_results="Full analysis text...",
    file_format="markdown"  # or "json"
)
```

### Generate Task CSV

```python
from src.orchestrator_with_attachments import generate_summary_csv

file_bytes, filename = await generate_summary_csv(
    tasks=[
        {"name": "Fix", "priority": "High", "effort": "2d", "impact": "High", "status": "Pending"},
    ]
)
```

## Content Types

The handler automatically detects content type:

| Extension | Content Type |
|-----------|--------------|
| .txt | text/plain |
| .md | text/markdown |
| .json | application/json |
| .csv | text/csv |
| .pdf | application/pdf |
| .png | image/png |
| .jpg | image/jpeg |

## Error Handling

Files are validated before sending:

```python
handler = AttachmentHandler(max_file_size=50*1024*1024)

# Validate size
if not handler.validate_file_size(file_size):
    logger.error("File too large")
    return None
```

## Best Practices

1. **Always provide filename** - Include file extension
2. **Set content type** - Use handler's `get_content_type()`
3. **Validate size** - Check before sending
4. **Error handling** - Gracefully handle failures
5. **User feedback** - Tell user about attached file

## Future Enhancements

- [ ] Support for inline images/documents
- [ ] Automatic PDF generation
- [ ] Streaming large files
- [ ] Archive multiple files (.zip)
- [ ] Direct file upload from GitHub

