"""
File Attachment Handler

Handles file upload and download for bot responses.
Supports sending files in bot responses.
"""

import logging
import os
from typing import Optional, Union, BinaryIO
from io import BytesIO

logger = logging.getLogger(__name__)


class AttachmentHandler:
    """Handler for file attachments in Poe bot responses"""
    
    def __init__(self, max_file_size: int = 50 * 1024 * 1024):
        """
        Initialize attachment handler.
        
        Args:
            max_file_size: Maximum file size in bytes (default 50MB)
        """
        self.max_file_size = max_file_size
    
    async def prepare_text_file(
        self,
        content: str,
        filename: str = "output.txt"
    ) -> tuple[bytes, str]:
        """
        Prepare text file for attachment.
        
        Args:
            content: Text content
            filename: Output filename
            
        Returns:
            Tuple of (file_bytes, filename)
        """
        try:
            file_bytes = content.encode('utf-8')
            
            if len(file_bytes) > self.max_file_size:
                logger.warning(f"File size {len(file_bytes)} exceeds limit")
                return None, None
            
            return file_bytes, filename
        
        except Exception as e:
            logger.exception(f"Error preparing text file: {e}")
            return None, None
    
    async def prepare_markdown_file(
        self,
        content: str,
        filename: str = "report.md"
    ) -> tuple[bytes, str]:
        """
        Prepare markdown file for attachment.
        
        Args:
            content: Markdown content
            filename: Output filename
            
        Returns:
            Tuple of (file_bytes, filename)
        """
        return await self.prepare_text_file(content, filename)
    
    async def prepare_json_file(
        self,
        data: dict,
        filename: str = "data.json"
    ) -> tuple[bytes, str]:
        """
        Prepare JSON file for attachment.
        
        Args:
            data: Dictionary to convert to JSON
            filename: Output filename
            
        Returns:
            Tuple of (file_bytes, filename)
        """
        try:
            import json
            json_str = json.dumps(data, indent=2)
            return await self.prepare_text_file(json_str, filename)
        
        except Exception as e:
            logger.exception(f"Error preparing JSON file: {e}")
            return None, None
    
    async def prepare_csv_file(
        self,
        headers: list[str],
        rows: list[list],
        filename: str = "data.csv"
    ) -> tuple[bytes, str]:
        """
        Prepare CSV file for attachment.
        
        Args:
            headers: Column headers
            rows: List of rows (each row is a list)
            filename: Output filename
            
        Returns:
            Tuple of (file_bytes, filename)
        """
        try:
            import csv
            from io import StringIO
            
            output = StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow(headers)
            
            # Write rows
            for row in rows:
                writer.writerow(row)
            
            csv_str = output.getvalue()
            return await self.prepare_text_file(csv_str, filename)
        
        except Exception as e:
            logger.exception(f"Error preparing CSV file: {e}")
            return None, None
    
    def validate_file_size(self, file_size: int) -> bool:
        """Validate file size is within limits"""
        return file_size <= self.max_file_size
    
    def get_content_type(self, filename: str) -> str:
        """Get MIME content type based on filename"""
        ext = os.path.splitext(filename)[1].lower()
        
        content_types = {
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.json': 'application/json',
            '.csv': 'text/csv',
            '.pdf': 'application/pdf',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.zip': 'application/zip',
        }
        
        return content_types.get(ext, 'application/octet-stream')
