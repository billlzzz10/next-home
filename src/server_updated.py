#!/usr/bin/env python3
"""
Updated BL1NK Skill MCP Server
With Bot Generation & Claude Tools
"""

import os, sys, logging, json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from src.bot_tools import BotGenerationTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Tool:
    """Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]

class BL1NKSkillMCPServer:
    """
    Updated MCP Server with Bot & Script Generation
    """
    
    def __init__(self):
        self.name = "bl1nk-skill-mcp-server"
        self.version = "2.0.0"  # Updated version
        self.tools = self._init_tools()
        self.bot_tools = BotGenerationTools()
    
    def _init_tools(self) -> List[Tool]:
        """Initialize all available tools"""
        return [
            # Original Tools
            Tool(
                name="list_skills",
                description="List all available BL1NK skills",
                input_schema={
                    "type": "object",
                    "properties": {
                        "phase": {
                            "type": "string",
                            "enum": ["critical", "integration", "platform", "advanced"],
                            "description": "Filter by skill phase"
                        }
                    }
                }
            ),
            Tool(
                name="run_skill",
                description="Execute a BL1NK skill",
                input_schema={
                    "type": "object",
                    "properties": {
                        "skill_name": {"type": "string", "description": "Skill name"},
                        "params": {"type": "object", "description": "Skill parameters"}
                    },
                    "required": ["skill_name"]
                }
            ),
            Tool(
                name="get_skill_info",
                description="Get information about a skill",
                input_schema={
                    "type": "object",
                    "properties": {
                        "skill_name": {"type": "string", "description": "Skill name"}
                    },
                    "required": ["skill_name"]
                }
            ),
            # NEW: Bot Generation Tools
            Tool(
                name="create_poe_script_bot",
                description="Create a new Poe script bot",
                input_schema={
                    "type": "object",
                    "properties": {
                        "bot_name": {"type": "string"},
                        "description": {"type": "string"},
                        "language": {"type": "string", "enum": ["python", "javascript"]}
                    },
                    "required": ["bot_name", "description"]
                }
            ),
            Tool(
                name="create_poe_canvas_bot",
                description="Create a Poe canvas bot (UI-based)",
                input_schema={
                    "type": "object",
                    "properties": {
                        "bot_name": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["bot_name", "description"]
                }
            ),
            Tool(
                name="generate_prompt",
                description="Generate optimized prompt for AI",
                input_schema={
                    "type": "object",
                    "properties": {
                        "prompt_name": {"type": "string"},
                        "description": {"type": "string"},
                        "use_case": {"type": "string"},
                        "style": {"type": "string", "enum": ["instruction-based", "conversational", "technical"]}
                    },
                    "required": ["prompt_name", "use_case"]
                }
            ),
            Tool(
                name="generate_script",
                description="Generate a script file",
                input_schema={
                    "type": "object",
                    "properties": {
                        "script_name": {"type": "string"},
                        "script_type": {"type": "string"},
                        "description": {"type": "string"},
                        "language": {"type": "string", "enum": ["python", "javascript", "bash"]}
                    },
                    "required": ["script_name", "script_type", "language"]
                }
            ),
            Tool(
                name="create_claude_project",
                description="Create a Claude project with context and instructions",
                input_schema={
                    "type": "object",
                    "properties": {
                        "project_name": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["project_name", "description"]
                }
            ),
            Tool(
                name="create_claude_plugin",
                description="Create a Claude plugin",
                input_schema={
                    "type": "object",
                    "properties": {
                        "plugin_name": {"type": "string"},
                        "description": {"type": "string"},
                        "capabilities": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["plugin_name", "description", "capabilities"]
                }
            ),
            Tool(
                name="list_bots",
                description="List all created bots",
                input_schema={
                    "type": "object",
                    "properties": {
                        "filter_type": {"type": "string"}
                    }
                }
            ),
            Tool(
                name="list_templates",
                description="List available bot templates",
                input_schema={"type": "object"}
            ),
            Tool(
                name="get_reference_poe",
                description="Get Poe protocol reference and best practices",
                input_schema={"type": "object"}
            ),
            Tool(
                name="test_bot",
                description="Test a bot with sample input",
                input_schema={
                    "type": "object",
                    "properties": {
                        "bot_id": {"type": "string"},
                        "test_input": {"type": "string"}
                    },
                    "required": ["bot_id", "test_input"]
                }
            ),
            Tool(
                name="fix_bot",
                description="Fix issues in a bot",
                input_schema={
                    "type": "object",
                    "properties": {
                        "bot_id": {"type": "string"},
                        "issue_description": {"type": "string"}
                    },
                    "required": ["bot_id", "issue_description"]
                }
            ),
        ]
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get all tools as dict"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in self.tools
        ]
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name"""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool"""
        tool = self.get_tool(tool_name)
        if not tool:
            return {"error": f"Tool '{tool_name}' not found"}
        
        # Original Skills Tools
        if tool_name == "list_skills":
            return self._list_skills(kwargs.get("phase"))
        elif tool_name == "run_skill":
            return self._run_skill(kwargs.get("skill_name"), kwargs.get("params"))
        elif tool_name == "get_skill_info":
            return self._get_skill_info(kwargs.get("skill_name"))
        
        # Bot Generation Tools
        elif tool_name == "create_poe_script_bot":
            return self.bot_tools.create_poe_script_bot(
                kwargs.get("bot_name"),
                kwargs.get("description"),
                kwargs.get("language", "python")
            )
        elif tool_name == "create_poe_canvas_bot":
            return self.bot_tools.create_poe_canvas_bot(
                kwargs.get("bot_name"),
                kwargs.get("description")
            )
        elif tool_name == "generate_prompt":
            return self.bot_tools.generate_prompt(
                kwargs.get("prompt_name"),
                kwargs.get("description", ""),
                kwargs.get("use_case"),
                kwargs.get("style", "instruction-based")
            )
        elif tool_name == "generate_script":
            return self.bot_tools.generate_script(
                kwargs.get("script_name"),
                kwargs.get("script_type"),
                kwargs.get("description", ""),
                kwargs.get("language", "python")
            )
        elif tool_name == "create_claude_project":
            return self.bot_tools.create_claude_project(
                kwargs.get("project_name"),
                kwargs.get("description")
            )
        elif tool_name == "create_claude_plugin":
            return self.bot_tools.create_claude_plugin(
                kwargs.get("plugin_name"),
                kwargs.get("description"),
                kwargs.get("capabilities", [])
            )
        elif tool_name == "list_bots":
            return {
                "bots": self.bot_tools.list_bots(kwargs.get("filter_type")),
                "total": len(self.bot_tools.bots)
            }
        elif tool_name == "list_templates":
            return {
                "templates": self.bot_tools.list_templates(),
                "total": len(self.bot_tools.templates)
            }
        elif tool_name == "get_reference_poe":
            return self.bot_tools.get_reference_poe()
        elif tool_name == "test_bot":
            return self.bot_tools.test_bot(
                kwargs.get("bot_id"),
                kwargs.get("test_input")
            )
        elif tool_name == "fix_bot":
            return self.bot_tools.fix_bot(
                kwargs.get("bot_id"),
                kwargs.get("issue_description")
            )
        
        return {"error": "Unknown tool"}
    
    def _list_skills(self, phase: Optional[str] = None) -> Dict[str, Any]:
        """List all skills"""
        skills = {
            "critical": [
                {"name": "text-processor", "description": "Text analysis & transformation"},
                {"name": "log-analyzer", "description": "Log parsing & analysis"},
                {"name": "notification-router", "description": "Multi-channel notifications"},
            ],
            "integration": [
                {"name": "github-repo-analyzer", "description": "GitHub repository health"},
                {"name": "prompt-optimizer", "description": "LLM prompt optimization"},
                {"name": "poe-bot-generator", "description": "POE protocol bot scaffolding"},
            ],
            "platform": [
                {"name": "code-analyzer", "description": "Code quality analysis"},
                {"name": "skill-chain-executor", "description": "Multi-skill orchestration"},
                {"name": "document-generator", "description": "Auto documentation"},
            ],
            "advanced": [
                {"name": "test-generator", "description": "Automated test generation"},
            ]
        }
        
        if phase:
            return {"phase": phase, "skills": skills.get(phase, [])}
        
        all_skills = []
        for p, s in skills.items():
            for skill in s:
                skill["phase"] = p
                all_skills.append(skill)
        
        return {"total": len(all_skills), "skills": all_skills}
    
    def _run_skill(self, skill_name: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Run a skill"""
        return {
            "status": "running",
            "skill": skill_name,
            "params": params or {},
            "message": f"Executing skill '{skill_name}'"
        }
    
    def _get_skill_info(self, skill_name: str) -> Dict[str, Any]:
        """Get skill information"""
        all_skills = self._list_skills()["skills"]
        for skill in all_skills:
            if skill["name"] == skill_name:
                return {"found": True, "skill": skill}
        
        return {"found": False, "error": f"Skill '{skill_name}' not found"}
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": self.name,
            "version": self.version,
            "tools": len(self.tools),
            "status": "ready",
            "categories": {
                "skills": 3,
                "bot_generation": 5,
                "template_management": 2,
                "testing": 2
            }
        }

# Global server instance
_server = None

def get_server() -> BL1NKSkillMCPServer:
    """Get or create server instance"""
    global _server
    if _server is None:
        _server = BL1NKSkillMCPServer()
    return _server

def main():
    """Main entry point"""
    logger.info("🚀 Starting BL1NK Skill MCP Server v2.0.0...")
    
    server = get_server()
    info = server.get_server_info()
    
    logger.info(f"Server: {info['name']} v{info['version']}")
    logger.info(f"Tools: {info['tools']}")
    logger.info(f"Status: {info['status']}")
    logger.info(f"✅ Server initialized and ready")

if __name__ == "__main__":
    main()
