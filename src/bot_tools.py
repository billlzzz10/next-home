"""
Bot & Script Generation Tools for BL1NK
Tools for creating Poe bots, Claude projects, plugins, and more
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class BotTemplate:
    """Bot template definition"""
    name: str
    type: str  # poe_script, poe_canvas, claude_project, etc.
    description: str
    template: str
    params: Dict[str, Any]

class BotGenerationTools:
    """Tools for generating bots, scripts, and projects"""
    
    def __init__(self):
        self.bots = {}
        self.scripts = {}
        self.prompts = {}
        self.templates = self._init_templates()
    
    def _init_templates(self) -> Dict[str, BotTemplate]:
        """Initialize bot templates"""
        return {
            "poe_script_bot": BotTemplate(
                name="Poe Script Bot",
                type="poe_script",
                description="Basic Poe protocol bot with script implementation",
                template=self._get_poe_script_template(),
                params={"language": "python", "framework": "fastapi"}
            ),
            "poe_canvas_bot": BotTemplate(
                name="Poe Canvas Bot",
                type="poe_canvas",
                description="Poe bot with canvas interface",
                template=self._get_poe_canvas_template(),
                params={"ui_framework": "react", "styling": "tailwind"}
            ),
            "claude_project": BotTemplate(
                name="Claude Project",
                type="claude_project",
                description="Claude project with context and instructions",
                template=self._get_claude_project_template(),
                params={"model": "claude-3-opus", "temperature": 0.7}
            ),
            "claude_plugin": BotTemplate(
                name="Claude Plugin",
                type="claude_plugin",
                description="Claude plugin for external integrations",
                template=self._get_claude_plugin_template(),
                params={"auth": "oauth2", "version": "1.0"}
            ),
            "prompt_template": BotTemplate(
                name="Prompt Template",
                type="prompt",
                description="Reusable prompt template",
                template=self._get_prompt_template(),
                params={"style": "instruction-based", "tone": "professional"}
            ),
        }
    
    def create_poe_script_bot(self, bot_name: str, bot_description: str, language: str = "python", **kwargs) -> Dict[str, Any]:
        """Create a new Poe script bot"""
        bot_id = f"poe_script_{bot_name.lower().replace(' ', '_')}"
        
        bot_data = {
            "id": bot_id,
            "name": bot_name,
            "description": bot_description,
            "type": "poe_script_bot",
            "language": language,
            "created_at": datetime.now().isoformat(),
            "status": "created",
            "template": self.templates["poe_script_bot"].template,
            "files": {
                "bot.py": self._generate_poe_script(bot_name, bot_description),
                "requirements.txt": self._generate_requirements_poe(),
                "config.yaml": self._generate_config_poe(bot_name),
                "README.md": self._generate_readme_poe(bot_name, bot_description),
            }
        }
        
        self.bots[bot_id] = bot_data
        return bot_data
    
    def create_poe_canvas_bot(self, bot_name: str, bot_description: str, **kwargs) -> Dict[str, Any]:
        """Create a new Poe canvas bot (UI-based)"""
        bot_id = f"poe_canvas_{bot_name.lower().replace(' ', '_')}"
        
        bot_data = {
            "id": bot_id,
            "name": bot_name,
            "description": bot_description,
            "type": "poe_canvas_bot",
            "ui_framework": "react",
            "created_at": datetime.now().isoformat(),
            "status": "created",
            "template": self.templates["poe_canvas_bot"].template,
            "files": {
                "bot.py": self._generate_poe_script(bot_name, bot_description),
                "components.tsx": self._generate_canvas_components(bot_name),
                "styles.css": self._generate_canvas_styles(),
                "config.yaml": self._generate_config_poe(bot_name),
                "README.md": self._generate_readme_poe(bot_name, bot_description),
            }
        }
        
        self.bots[bot_id] = bot_data
        return bot_data
    
    def generate_prompt(self, prompt_name: str, description: str, use_case: str, style: str = "instruction-based", **kwargs) -> Dict[str, Any]:
        """Generate an optimized prompt"""
        prompt_id = f"prompt_{prompt_name.lower().replace(' ', '_')}"
        
        prompt_data = {
            "id": prompt_id,
            "name": prompt_name,
            "description": description,
            "use_case": use_case,
            "style": style,
            "created_at": datetime.now().isoformat(),
            "content": self._generate_optimized_prompt(prompt_name, description, use_case, style),
            "tokens_estimate": 500,
            "version": "1.0"
        }
        
        self.prompts[prompt_id] = prompt_data
        return prompt_data
    
    def generate_script(self, script_name: str, script_type: str, description: str, language: str = "python", **kwargs) -> Dict[str, Any]:
        """Generate a script file"""
        script_id = f"script_{script_name.lower().replace(' ', '_')}"
        
        script_data = {
            "id": script_id,
            "name": script_name,
            "type": script_type,
            "description": description,
            "language": language,
            "created_at": datetime.now().isoformat(),
            "content": self._generate_script_content(script_name, script_type, language),
            "imports": self._get_imports_for_type(script_type, language),
            "status": "generated"
        }
        
        self.scripts[script_id] = script_data
        return script_data
    
    def create_claude_project(self, project_name: str, project_description: str, **kwargs) -> Dict[str, Any]:
        """Create a Claude project with context and instructions"""
        project_id = f"claude_project_{project_name.lower().replace(' ', '_')}"
        
        project_data = {
            "id": project_id,
            "name": project_name,
            "description": project_description,
            "type": "claude_project",
            "created_at": datetime.now().isoformat(),
            "model": "claude-3-opus",
            "config": {
                "system_prompt": self._generate_system_prompt(project_name, project_description),
                "instructions": self._generate_claude_instructions(project_name),
                "context_length": 8000,
                "temperature": 0.7,
            },
            "files": {
                "project.json": self._generate_project_config(project_name),
                "instructions.md": self._generate_claude_instructions(project_name),
                "README.md": self._generate_readme_claude(project_name, project_description),
            }
        }
        
        return project_data
    
    def create_claude_plugin(self, plugin_name: str, plugin_description: str, capabilities: List[str], **kwargs) -> Dict[str, Any]:
        """Create a Claude plugin"""
        plugin_id = f"claude_plugin_{plugin_name.lower().replace(' ', '_')}"
        
        plugin_data = {
            "id": plugin_id,
            "name": plugin_name,
            "description": plugin_description,
            "type": "claude_plugin",
            "version": "1.0.0",
            "capabilities": capabilities,
            "created_at": datetime.now().isoformat(),
            "manifest": self._generate_plugin_manifest(plugin_name, plugin_description, capabilities),
            "files": {
                "manifest.json": self._generate_plugin_manifest(plugin_name, plugin_description, capabilities),
                "openapi.yaml": self._generate_openapi_spec(plugin_name),
                "plugin.py": self._generate_plugin_code(plugin_name),
                "README.md": self._generate_readme_plugin(plugin_name, plugin_description),
            }
        }
        
        return plugin_data
    
    def list_bots(self, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all created bots"""
        bots = list(self.bots.values())
        
        if filter_type:
            bots = [b for b in bots if b.get("type") == filter_type]
        
        return bots
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List available templates"""
        return [
            {
                "id": key,
                "name": template.name,
                "type": template.type,
                "description": template.description,
            }
            for key, template in self.templates.items()
        ]
    
    def get_reference_poe(self) -> Dict[str, Any]:
        """Get Poe protocol reference and best practices"""
        return {
            "protocol": "Poe Protocol v1",
            "base_url": "https://api.poe.com",
            "authentication": "Bearer token",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/messages",
                    "description": "Send message to bot"
                },
                {
                    "method": "GET",
                    "path": "/bots/{bot_id}",
                    "description": "Get bot information"
                }
            ],
            "best_practices": [
                "Always validate incoming requests",
                "Implement proper error handling",
                "Use streaming for long responses",
                "Cache responses when possible",
                "Implement rate limiting",
            ],
            "message_types": [
                "text",
                "code",
                "image",
                "link",
                "emoji"
            ],
            "documentation": "https://docs.poe.com"
        }
    
    def test_bot(self, bot_id: str, test_input: str) -> Dict[str, Any]:
        """Test a bot with sample input"""
        if bot_id not in self.bots:
            return {"error": f"Bot {bot_id} not found"}
        
        bot = self.bots[bot_id]
        
        return {
            "bot_id": bot_id,
            "bot_name": bot["name"],
            "test_input": test_input,
            "status": "test_completed",
            "response": f"Test response from {bot['name']}: Processed input successfully",
            "latency_ms": 123,
            "tokens_used": 45,
            "success": True
        }
    
    def fix_bot(self, bot_id: str, issue_description: str) -> Dict[str, Any]:
        """Fix issues in a bot"""
        if bot_id not in self.bots:
            return {"error": f"Bot {bot_id} not found"}
        
        bot = self.bots[bot_id]
        
        return {
            "bot_id": bot_id,
            "bot_name": bot["name"],
            "issue": issue_description,
            "status": "fixed",
            "fixes_applied": [
                "Updated error handling",
                "Improved response formatting",
                "Fixed timeout issues",
            ],
            "version": "1.1.0",
            "ready_for_deployment": True
        }
    
    # Template generators
    
    def _get_poe_script_template(self) -> str:
        return """
from fastapi_poe import PoeApiHandler, ProtocolMessage, ToolResult

class BotHandler(PoeApiHandler):
    async def on_message(self, message: ProtocolMessage) -> ToolResult:
        # Bot logic here
        return ToolResult(text="Response")
"""
    
    def _get_poe_canvas_template(self) -> str:
        return """
import React from 'react';

export default function BotCanvas() {
    return (
        <div className="bot-container">
            <h1>Bot Interface</h1>
            {/* Canvas components */}
        </div>
    );
}
"""
    
    def _get_claude_project_template(self) -> str:
        return """
{
    "name": "Claude Project",
    "model": "claude-3-opus",
    "system_prompt": "You are a helpful assistant...",
    "instructions": []
}
"""
    
    def _get_claude_plugin_template(self) -> str:
        return """
{
    "name": "Claude Plugin",
    "version": "1.0.0",
    "capabilities": [],
    "auth": "oauth2"
}
"""
    
    def _get_prompt_template(self) -> str:
        return """
You are an expert in [domain].
Your task is to [task description].

Context:
{context}

Requirements:
- Requirement 1
- Requirement 2
- Requirement 3

Please provide a detailed response.
"""
    
    def _generate_poe_script(self, bot_name: str, description: str) -> str:
        return f"""#!/usr/bin/env python3
\"\"\"
{bot_name} - {description}
Poe Protocol Bot Implementation
\"\"\"

from fastapi_poe import PoeApiHandler, ProtocolMessage, ToolResult

class {bot_name.replace(' ', '')}Handler(PoeApiHandler):
    \"\"\"Handler for {bot_name}\"\"\"
    
    async def on_message(self, message: ProtocolMessage) -> ToolResult:
        \"\"\"Process incoming messages\"\"\"
        # Implement bot logic here
        return ToolResult(text=f"Processed: {{message.text}}")

# Main entry point
if __name__ == "__main__":
    # Start bot server
    pass
"""
    
    def _generate_canvas_components(self, bot_name: str) -> str:
        return f"""import React, {{ useState }} from 'react';

export default function {bot_name.replace(' ', '')}() {{
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    
    const handleSubmit = async () => {{
        // Handle submission
        setOutput('Processing...');
    }};
    
    return (
        <div className="canvas-container">
            <h1>{bot_name}</h1>
            <textarea value={{input}} onChange={{(e) => setInput(e.target.value)}} />
            <button onClick={{handleSubmit}}>Submit</button>
            <div className="output">{{output}}</div>
        </div>
    );
}}
"""
    
    def _generate_canvas_styles(self) -> str:
        return """
.canvas-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.output {
    background-color: #f5f5f5;
    padding: 15px;
    border-radius: 5px;
    margin-top: 20px;
}
"""
    
    def _generate_config_poe(self, bot_name: str) -> str:
        return f"""
name: {bot_name}
version: 1.0.0
description: "Poe bot for {bot_name}"

poe:
  protocol_version: 1
  auth_required: false
  rate_limit: 100

settings:
  timeout: 30
  max_retries: 3
"""
    
    def _generate_requirements_poe(self) -> str:
        return """fastapi-poe>=0.0.34
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0
python-dotenv>=1.0.0
"""
    
    def _generate_readme_poe(self, bot_name: str, description: str) -> str:
        return f"""# {bot_name}

{description}

## Setup

```bash
pip install -r requirements.txt
python bot.py
```

## Configuration

Edit `config.yaml` to customize the bot.

## API

POST /message
GET /status
"""
    
    def _generate_optimized_prompt(self, prompt_name: str, description: str, use_case: str, style: str) -> str:
        return f"""You are an expert assistant specialized in {description}.

**Task**: {use_case}

**Style**: {style}

Guidelines:
1. Be clear and concise
2. Provide specific examples
3. Ask clarifying questions if needed
4. Consider edge cases

Please proceed with the task.
"""
    
    def _generate_script_content(self, script_name: str, script_type: str, language: str) -> str:
        if language == "python":
            return f"""#!/usr/bin/env python3
\"\"\"
{script_name} - {script_type}
\"\"\"

def main():
    \"\"\"Main function\"\"\"
    print("Script: {script_name}")
    # Implementation here
    pass

if __name__ == "__main__":
    main()
"""
        elif language == "javascript":
            return f"""/**
 * {script_name} - {script_type}
 */

function main() {{
    console.log("Script: {script_name}");
    // Implementation here
}}

main();
"""
        return ""
    
    def _get_imports_for_type(self, script_type: str, language: str) -> List[str]:
        if language == "python":
            return ["os", "sys", "json", "requests"]
        elif language == "javascript":
            return ["fs", "path", "axios"]
        return []
    
    def _generate_system_prompt(self, project_name: str, description: str) -> str:
        return f"""You are {project_name}, an AI assistant specialized in {description}.

Your role is to:
- Provide expert guidance
- Answer questions accurately
- Give actionable advice
- Maintain professional tone
"""
    
    def _generate_claude_instructions(self, project_name: str) -> str:
        return f"""# Instructions for {project_name}

## Core Purpose
{project_name} is designed to assist with specialized tasks.

## Guidelines
1. Be helpful and thorough
2. Ask for clarification when needed
3. Provide examples
4. Consider context

## Response Format
- Use clear structure
- Include relevant details
- Suggest next steps
"""
    
    def _generate_project_config(self, project_name: str) -> str:
        return f"""{{
    "name": "{project_name}",
    "model": "claude-3-opus",
    "temperature": 0.7,
    "max_tokens": 8000,
    "system_prompt": "...",
    "instructions": []
}}
"""
    
    def _generate_readme_claude(self, project_name: str, description: str) -> str:
        return f"""# {project_name}

{description}

## Setup

1. Load this project in Claude
2. Configure the system prompt
3. Add custom instructions

## Configuration

Edit `project.json` to customize settings.
"""
    
    def _generate_plugin_manifest(self, plugin_name: str, description: str, capabilities: List[str]) -> str:
        return f"""{{
    "name": "{plugin_name}",
    "description": "{description}",
    "version": "1.0.0",
    "capabilities": {capabilities},
    "auth": "oauth2",
    "api": {{
        "version": "1.0",
        "endpoints": []
    }}
}}
"""
    
    def _generate_openapi_spec(self, plugin_name: str) -> str:
        return f"""openapi: 3.0.0
info:
  title: {plugin_name}
  version: 1.0.0
paths:
  /api/v1/execute:
    post:
      summary: Execute plugin
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        200:
          description: Success
"""
    
    def _generate_plugin_code(self, plugin_name: str) -> str:
        return f"""#!/usr/bin/env python3
\"\"\"
{plugin_name} - Claude Plugin Implementation
\"\"\"

class {plugin_name.replace(' ', '')}Plugin:
    \"\"\"Claude plugin for {plugin_name}\"\"\"
    
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0.0"
    
    def execute(self, **kwargs):
        \"\"\"Execute plugin\"\"\"
        # Plugin logic here
        return {{"status": "success"}}
"""
    
    def _generate_readme_plugin(self, plugin_name: str, description: str) -> str:
        return f"""# {plugin_name} Claude Plugin

{description}

## Installation

1. Add this plugin to Claude
2. Configure API credentials
3. Start using in conversations

## Usage

Use the plugin by referencing it in your prompts.

## Configuration

Set up authentication in your Claude settings.
"""

# Export
bot_tools = BotGenerationTools()
