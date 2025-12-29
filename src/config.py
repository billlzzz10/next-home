"""
Configuration for BL1NK Skill MCP Server
"""

import os
from typing import Optional

class Config:
    """Server configuration"""
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API settings
    API_TITLE: str = "BL1NK Skill MCP Server"
    API_VERSION: str = "1.0.0"
    
    # Skills configuration
    SKILLS_DIR: str = os.getenv("SKILLS_DIR", "./skills")
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    
    # AWS settings (optional)
    AWS_REGION: Optional[str] = os.getenv("AWS_REGION")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    @staticmethod
    def get_config() -> 'Config':
        """Get configuration instance"""
        return Config()

config = Config.get_config()
