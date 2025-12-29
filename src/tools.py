"""
MCP Tools for BL1NK Skills
"""

from typing import List, Dict, Any

AVAILABLE_TOOLS = [
    {
        "name": "list_skills",
        "description": "List all available skills",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phase": {
                    "type": "string",
                    "description": "Filter by skill phase (critical, integration, platform, advanced)"
                }
            }
        }
    },
    {
        "name": "run_skill",
        "description": "Execute a specific skill",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill to run"
                },
                "params": {
                    "type": "object",
                    "description": "Skill parameters"
                }
            },
            "required": ["skill_name"]
        }
    },
    {
        "name": "get_skill_info",
        "description": "Get information about a specific skill",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill"
                }
            },
            "required": ["skill_name"]
        }
    }
]

def get_tools() -> List[Dict[str, Any]]:
    """Get all available tools"""
    return AVAILABLE_TOOLS

def get_tool_by_name(name: str) -> Dict[str, Any]:
    """Get tool definition by name"""
    for tool in AVAILABLE_TOOLS:
        if tool["name"] == name:
            return tool
    return None
