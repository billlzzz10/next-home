"""
Enhanced Poe Bot with Skill Support

Combines original orchestrator with skill/plugin system:
1. Route queries to skills or original analyzer
2. Execute skills as inline plugins
3. Chain skills together
4. Expose skill directory
"""

import os
import logging
from typing import Optional, AsyncGenerator
import fastapi_poe as fp
from fastapi import FastAPI, HTTPException

from src.bot import Bl1nkArchitectBot, create_app as create_base_app
from src.poe_plugin_manager import (
    get_skill_router_bot,
    get_skill_bot_factory,
    initialize_skill_bots,
    PoeSkillBot,
)

logger = logging.getLogger(__name__)


class Bl1nkArchitectWithSkillsBot(Bl1nkArchitectBot):
    """Enhanced bot with skill/plugin support"""
    
    def __init__(self):
        super().__init__()
        self.skill_router_bot = None
        self.skill_factory = get_skill_bot_factory()
        self.skills_initialized = False
    
    async def initialize_skills(self):
        """Lazy initialize skills"""
        if not self.skills_initialized:
            try:
                await initialize_skill_bots()
                self.skill_router_bot = get_skill_router_bot()
                self.skills_initialized = True
                logger.info("Skills initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing skills: {e}")
                self.skills_initialized = True  # Mark as attempted
    
    async def get_response(
        self,
        request: fp.QueryRequest
    ) -> AsyncGenerator[fp.ProtocolMessage, None]:
        """Handle query - route to skill or original analyzer"""
        
        try:
            yield fp.MetaResponse(
                content_type="text/markdown",
                linkify=True,
                suggested_replies=False
            )
            
            user_id = request.user_id
            last_message = request.query[-1].content if request.query else ""
            
            logger.info(f"Query: {last_message[:50]}...")
            
            # Initialize skills on first request
            await self.initialize_skills()
            
            # Check for skill-related commands
            if self._is_skill_command(last_message):
                # Route to skill router bot
                if self.skill_router_bot:
                    async for response in self.skill_router_bot.get_response(request):
                        yield response
                else:
                    yield fp.ErrorResponse(
                        text="Skills not available",
                        allow_retry=True
                    )
                return
            
            # Try to route to appropriate skill
            if self._should_use_skill(last_message):
                if self.skill_router_bot:
                    async for response in self.skill_router_bot.get_response(request):
                        yield response
                    return
            
            # Fall back to original analyzer
            async for response in super().get_response(request):
                yield response
        
        except Exception as e:
            logger.exception(f"Error: {e}")
            yield fp.ErrorResponse(
                text=f"Error: {str(e)}",
                allow_retry=True
            )
    
    def _is_skill_command(self, message: str) -> bool:
        """Check if message is a skill command"""
        skill_commands = [
            "list skills",
            "show skills",
            "search skills",
            "available skills",
            "@skill",
            "/skill",
        ]
        message_lower = message.lower()
        return any(cmd in message_lower for cmd in skill_commands)
    
    def _should_use_skill(self, message: str) -> bool:
        """Determine if query should use skill instead of analyzer"""
        skill_keywords = [
            "notification",
            "slack",
            "linear",
            "clickup",
            "widget",
            "report",
            "plugin",
            "script",
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in skill_keywords)
    
    async def get_settings(
        self,
        setting: fp.SettingsRequest
    ) -> fp.SettingsResponse:
        """Return enhanced settings with skill info"""
        
        await self.initialize_skills()
        
        # Get base settings
        base_settings = await super().get_settings(setting)
        
        # Enhance introduction message with skills
        skills_count = len(self.skill_factory.get_all_bots())
        
        enhanced_intro = (
            base_settings.introduction_message + 
            f"\n\n**Skills Available:** {skills_count} plugins loaded\n"
            f"Type **list skills** to see available plugins"
        )
        
        return fp.SettingsResponse(
            server_bot_dependencies=base_settings.server_bot_dependencies,
            allow_attachments=base_settings.allow_attachments,
            expand_text_attachments=base_settings.expand_text_attachments,
            enable_image_comprehension=base_settings.enable_image_comprehension,
            introduction_message=enhanced_intro,
            response_version=base_settings.response_version,
        )


def create_app_with_skills() -> FastAPI:
    """Create FastAPI app with skill support"""
    
    # Create base app
    app = create_base_app()
    
    # Remove original bot
    # Create enhanced bot with skills
    bot = Bl1nkArchitectWithSkillsBot()
    
    # Setup Poe with enhanced bot
    access_key = os.getenv("POE_ACCESS_KEY")
    if not access_key:
        raise ValueError("POE_ACCESS_KEY environment variable not set")
    
    fp.make_app(
        bot,
        access_key=access_key,
        app=app,
        allow_without_key=False,
    )
    
    # Add skill management endpoints
    
    @app.get("/skills")
    async def list_skills():
        """List available skills"""
        factory = get_skill_bot_factory()
        return {
            "total": len(factory.get_all_bots()),
            "skills": list(factory.get_all_bots().keys())
        }
    
    @app.get("/skills/{skill_id}")
    async def get_skill(skill_id: str):
        """Get skill details"""
        factory = get_skill_bot_factory()
        skill_bot = factory.get_bot(skill_id)
        
        if not skill_bot:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        return {
            "id": skill_id,
            "description": skill_bot.bot.description if skill_bot.bot else "Loading..."
        }
    
    @app.post("/skills/{skill_id}/execute")
    async def execute_skill(skill_id: str, query: str):
        """Execute a skill"""
        factory = get_skill_bot_factory()
        skill_bot = factory.get_bot(skill_id)
        
        if not skill_bot:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        try:
            from src.skill_loader import execute_skill
            result = await execute_skill(skill_id, query)
            return {"result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    logger.info("Bot with skills support created")
    return app


if __name__ == "__main__":
    import uvicorn
    app = create_app_with_skills()
    uvicorn.run(app, host="0.0.0.0", port=8000)
