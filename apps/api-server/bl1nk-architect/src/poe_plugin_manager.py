"""
Poe Plugin Manager - Enable Skills as Poe Script Bots

Integrates Skill Loader with Poe Protocol to:
1. Create dynamic Poe bots from skills
2. Route queries to appropriate skill bots
3. Chain multiple skills together
4. Expose skills via Poe endpoints
5. Manage skill lifecycle within Poe
"""

import os
import logging
from typing import Dict, List, Optional, AsyncGenerator
import fastapi_poe as fp
from src.skill_loader import (
    get_skill_loader,
    load_skills,
    get_available_skills,
    search_skills,
    execute_skill,
    SkillBot
)

logger = logging.getLogger(__name__)


class PoeSkillRouter:
    """Route Poe queries to appropriate skill"""
    
    def __init__(self):
        self.loader = get_skill_loader()
        self.skill_bots: Dict[str, SkillBot] = {}
    
    async def initialize(self) -> int:
        """Load all skills"""
        count = await load_skills()
        self.skill_bots = self.loader.bots
        logger.info(f"Initialized {count} skill bots")
        return count
    
    async def route_to_skill(
        self,
        query: str,
        skill_hint: Optional[str] = None
    ) -> Optional[SkillBot]:
        """
        Route query to appropriate skill
        
        Priority:
        1. Explicit skill_hint parameter
        2. Skill mentioned in query
        3. Best match by keyword search
        """
        
        # If explicit hint provided, use it
        if skill_hint:
            bot = self.loader.get_bot(skill_hint)
            if bot:
                return bot
        
        # Search for skill mentioned in query
        results = await search_skills(query)
        if results:
            best_match = results[0]
            return self.loader.get_bot(best_match['id'])
        
        return None
    
    async def list_skills(self) -> List[Dict]:
        """List available skills"""
        return await get_available_skills()
    
    async def search(self, query: str) -> List[Dict]:
        """Search for skills"""
        return await search_skills(query)


class PoeSkillBot(fp.PoeBot):
    """Poe bot that executes skills"""
    
    def __init__(self):
        self.router = PoeSkillRouter()
        self.initialized = False
    
    async def initialize_skills(self):
        """Initialize skills (lazy load)"""
        if not self.initialized:
            await self.router.initialize()
            self.initialized = True
    
    async def get_response(
        self,
        request: fp.QueryRequest
    ) -> AsyncGenerator[fp.ProtocolMessage, None]:
        """Handle Poe query - route to skill or execute"""
        
        try:
            # Initialize skills if needed
            await self.initialize_skills()
            
            # Yield metadata
            yield fp.MetaResponse(
                content_type="text/markdown",
                linkify=True,
                suggested_replies=False
            )
            
            user_id = request.user_id
            last_message = request.query[-1].content if request.query else ""
            
            logger.info(f"Skill Bot Query from {user_id}: {last_message[:50]}...")
            
            # Check if querying for available skills
            if "list skills" in last_message.lower() or "show skills" in last_message.lower():
                yield from self._handle_list_skills()
                return
            
            if "search" in last_message.lower():
                yield from self._handle_search(last_message)
                return
            
            # Try to route to appropriate skill
            skill_bot = await self.router.route_to_skill(last_message)
            
            if not skill_bot:
                yield fp.PartialResponse(
                    text="❌ No matching skill found for your query.\n\n"
                         "Available skills:\n"
                )
                yield from self._handle_list_skills()
                return
            
            # Execute skill
            yield fp.PartialResponse(
                text=f"🔧 Executing skill: **{skill_bot.name}**\n\n"
            )
            
            result = await skill_bot.call_with_instructions(last_message)
            yield fp.PartialResponse(text=result)
        
        except Exception as e:
            logger.exception(f"Error in skill bot: {e}")
            yield fp.ErrorResponse(
                text=f"Error executing skill: {str(e)}",
                allow_retry=True
            )
    
    def _handle_list_skills(self) -> AsyncGenerator[fp.PartialResponse, None]:
        """List available skills"""
        async def _gen():
            skills = await self.router.list_skills()
            
            if not skills:
                yield fp.PartialResponse(text="No skills available")
                return
            
            for skill in skills:
                skill_text = f"""
## 🔧 {skill['id'].upper()}

**Description:** {skill['description']}

**Version:** {skill.get('version', 'Unknown')}

**Tags:** {', '.join(skill.get('tags', []))}

**Scripts:** {', '.join(skill.get('scripts', []))}

---
"""
                yield fp.PartialResponse(text=skill_text)
        
        return _gen()
    
    def _handle_search(self, query: str) -> AsyncGenerator[fp.PartialResponse, None]:
        """Search for skills"""
        async def _gen():
            # Extract search term
            search_term = query.replace("search", "").replace(":", "").strip()
            
            if not search_term:
                yield fp.PartialResponse(text="Please provide a search term")
                return
            
            results = await self.router.search(search_term)
            
            if not results:
                yield fp.PartialResponse(
                    text=f"No skills found matching: {search_term}"
                )
                return
            
            yield fp.PartialResponse(
                text=f"Found {len(results)} skill(s) matching '{search_term}':\n\n"
            )
            
            for result in results:
                result_text = f"""
### {result['id']}
{result['description']}

**Match Type:** {result['match_type']}
"""
                yield fp.PartialResponse(text=result_text)
        
        return _gen()
    
    async def get_settings(
        self,
        setting: fp.SettingsRequest
    ) -> fp.SettingsResponse:
        """Return bot settings"""
        await self.initialize_skills()
        
        # Get skill count
        skills = await self.router.list_skills()
        
        return fp.SettingsResponse(
            server_bot_dependencies={},
            allow_attachments=False,
            introduction_message=(
                f"🔧 **Poe Skill Bot**\n\n"
                f"I can execute {len(skills)} available Agent Skills.\n\n"
                f"Commands:\n"
                f"- **list skills** - Show all available skills\n"
                f"- **search: [term]** - Search for skills\n"
                f"- Or ask me to use a specific skill for your query\n\n"
                f"Available Skills: {', '.join(s['id'] for s in skills)}"
            ),
            response_version=1,
        )
    
    async def on_feedback(self, feedback: fp.FeedbackRequest) -> None:
        """Handle feedback"""
        logger.info(f"Feedback: {feedback.feedback_type} from {feedback.user_id}")
    
    async def on_error(self, error: fp.ErrorRequest) -> None:
        """Handle error"""
        logger.error(f"Error: {error.error_message} for message {error.message_id}")


class DynamicSkillBotFactory:
    """Factory to create individual Poe bots for each skill"""
    
    def __init__(self):
        self.loader = get_skill_loader()
        self.bots: Dict[str, "DynamicSkillPoeBot"] = {}
    
    async def initialize(self):
        """Initialize factory with all skills"""
        count = await load_skills()
        
        # Create individual bot for each skill
        skills = await get_available_skills()
        for skill in skills:
            self.bots[skill['id']] = DynamicSkillPoeBot(skill['id'])
        
        logger.info(f"Created {len(self.bots)} dynamic skill bots")
    
    def get_bot(self, skill_id: str) -> Optional["DynamicSkillPoeBot"]:
        """Get bot for skill"""
        return self.bots.get(skill_id)
    
    def get_all_bots(self) -> Dict[str, "DynamicSkillPoeBot"]:
        """Get all skill bots"""
        return self.bots


class DynamicSkillPoeBot(fp.PoeBot):
    """Individual Poe bot for a specific skill"""
    
    def __init__(self, skill_id: str):
        self.skill_id = skill_id
        self.loader = get_skill_loader()
        self.bot = None
    
    async def _ensure_loaded(self):
        """Ensure skill is loaded"""
        if not self.bot:
            self.bot = self.loader.get_bot(self.skill_id)
            if not self.bot:
                raise ValueError(f"Skill not found: {self.skill_id}")
    
    async def get_response(
        self,
        request: fp.QueryRequest
    ) -> AsyncGenerator[fp.ProtocolMessage, None]:
        """Handle query - execute specific skill"""
        
        try:
            await self._ensure_loaded()
            
            yield fp.MetaResponse(
                content_type="text/markdown",
                linkify=True
            )
            
            user_id = request.user_id
            last_message = request.query[-1].content if request.query else ""
            
            logger.info(f"Skill {self.skill_id} Query: {last_message[:50]}...")
            
            # Execute skill
            result = await execute_skill(self.skill_id, last_message)
            yield fp.PartialResponse(text=result)
        
        except Exception as e:
            logger.exception(f"Error in skill bot {self.skill_id}: {e}")
            yield fp.ErrorResponse(
                text=f"Error executing skill: {str(e)}",
                allow_retry=True
            )
    
    async def get_settings(
        self,
        setting: fp.SettingsRequest
    ) -> fp.SettingsResponse:
        """Return bot settings"""
        await self._ensure_loaded()
        
        if not self.bot:
            raise ValueError(f"Skill not found: {self.skill_id}")
        
        return fp.SettingsResponse(
            server_bot_dependencies={},
            allow_attachments=False,
            introduction_message=(
                f"🔧 **{self.skill_id}**\n\n"
                f"{self.bot.description}\n\n"
                f"Ask me to help with tasks related to this skill."
            ),
            response_version=1,
        )


# Global factory instance
_factory: Optional[DynamicSkillBotFactory] = None


def get_skill_bot_factory() -> DynamicSkillBotFactory:
    """Get or create skill bot factory"""
    global _factory
    if _factory is None:
        _factory = DynamicSkillBotFactory()
    return _factory


async def initialize_skill_bots() -> int:
    """Initialize all skill bots"""
    factory = get_skill_bot_factory()
    await factory.initialize()
    return len(factory.get_all_bots())


def get_skill_router_bot() -> PoeSkillBot:
    """Get the main router bot"""
    return PoeSkillBot()
