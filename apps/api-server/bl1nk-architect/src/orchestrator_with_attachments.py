"""
Orchestrator Extension - File Attachment Support

Allows workflow to send architecture report as downloadable file.
"""

import logging
from typing import AsyncGenerator, Optional

from src.attachment_handler import AttachmentHandler

logger = logging.getLogger(__name__)


async def create_architecture_report(
    repo_name: str,
    analysis_results: str,
    file_format: str = "markdown"
) -> tuple[bytes, str, str]:
    """
    Create architecture report file.
    
    Args:
        repo_name: Repository name
        analysis_results: Full analysis results
        file_format: Output format (markdown, json, html)
        
    Returns:
        Tuple of (file_bytes, filename, content_type)
    """
    
    handler = AttachmentHandler()
    
    if file_format == "markdown":
        # Wrap analysis in markdown template
        report_content = f"""# Architecture Analysis Report

**Repository**: {repo_name}

---

## Analysis Results

{analysis_results}

---

## Export Information

- Generated: Architecture Analysis Bot
- Format: Markdown
- Status: Complete

"""
        file_bytes, filename = await handler.prepare_markdown_file(
            report_content,
            filename=f"{repo_name}_architecture_analysis.md"
        )
        content_type = "text/markdown"
    
    elif file_format == "json":
        report_data = {
            "repository": repo_name,
            "analysis": analysis_results,
            "format": "json",
            "status": "complete"
        }
        file_bytes, filename = await handler.prepare_json_file(
            report_data,
            filename=f"{repo_name}_architecture_analysis.json"
        )
        content_type = "application/json"
    
    else:
        # Default to markdown
        file_bytes, filename = await handler.prepare_markdown_file(
            analysis_results,
            filename=f"{repo_name}_analysis.md"
        )
        content_type = "text/markdown"
    
    return file_bytes, filename, content_type


async def generate_summary_csv(
    tasks: list[dict],
    filename: str = "architecture_tasks.csv"
) -> tuple[bytes, str]:
    """
    Generate CSV file with architecture tasks.
    
    Args:
        tasks: List of task dictionaries
        filename: Output CSV filename
        
    Returns:
        Tuple of (file_bytes, filename)
    """
    
    handler = AttachmentHandler()
    
    # Extract headers
    headers = ["Task", "Priority", "Effort", "Impact", "Status"]
    
    # Build rows
    rows = []
    for task in tasks:
        rows.append([
            task.get("name", ""),
            task.get("priority", ""),
            task.get("effort", ""),
            task.get("impact", ""),
            task.get("status", "Pending"),
        ])
    
    file_bytes, _ = await handler.prepare_csv_file(
        headers,
        rows,
        filename
    )
    
    return file_bytes, filename
