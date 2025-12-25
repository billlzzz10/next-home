"""
Skill Loader API - Load and manage Agent Skills as Poe Script Bots

Enables Bl1nk Architect to:
1. Discover and load Skills from filesystem
2. Parse SKILL.md with YAML frontmatter
3. Execute Skills as dynamic Poe bots
4. Chain multiple skills together
5. Expose skills via Poe endpoints
"""

import os
import yaml
import logging
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import importlib.util
import sys

logger = logging.getLogger(__name__)


@dataclass
class SkillMetadata:
    """Skill metadata from SKILL.md frontmatter"""
    name: str
    description: str
    path: str
    version: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class SkillContent:
    """Complete skill content"""
    metadata: SkillMetadata
    instructions: str
    scripts: Dict[str, str] = None  # {filename: path}
    resources: Dict[str, str] = None  # {filename: path}
    
    def __post_init__(self):
        if self.scripts is None:
            self.scripts = {}
        if self.resources is None:
            self.resources = {}


class SkillDiscovery:
    """Discover and parse Skills from filesystem"""
    
    @staticmethod
    def find_skills(root_path: str = "/home/user/skills") -> List[Path]:
        """Find all SKILL.md files in directory"""
        skills = []
        root = Path(root_path)
        
        if not root.exists():
            logger.warning(f"Skills directory not found: {root_path}")
            return skills
        
        # Search for SKILL.md files
        for skill_file in root.rglob("SKILL.md"):
            skills.append(skill_file.parent)
        
        logger.info(f"Discovered {len(skills)} skills")
        return skills
    
    @staticmethod
    def parse_skill_file(skill_dir: Path) -> Optional[SkillContent]:
        """Parse SKILL.md and load skill metadata"""
        skill_file = skill_dir / "SKILL.md"
        
        if not skill_file.exists():
            logger.warning(f"SKILL.md not found in {skill_dir}")
            return None
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            if not content.startswith('---'):
                logger.error(f"Invalid SKILL.md format: {skill_file}")
                return None
            
            # Split frontmatter and content
            parts = content.split('---', 2)
            if len(parts) < 3:
                logger.error(f"Frontmatter not properly closed: {skill_file}")
                return None
            
            frontmatter_str = parts[1]
            instructions = parts[2].strip()
            
            # Parse YAML
            try:
                metadata_dict = yaml.safe_load(frontmatter_str)
            except yaml.YAMLError as e:
                logger.error(f"YAML parse error: {e}")
                return None
            
            # Create metadata
            metadata = SkillMetadata(
                name=metadata_dict.get('name', 'unknown'),
                description=metadata_dict.get('description', ''),
                path=str(skill_dir),
                version=metadata_dict.get('version'),
                author=metadata_dict.get('author'),
                tags=metadata_dict.get('tags', []),
                dependencies=metadata_dict.get('dependencies', [])
            )
            
            # Find scripts and resources
            scripts = SkillDiscovery._find_scripts(skill_dir)
            resources = SkillDiscovery._find_resources(skill_dir)
            
            return SkillContent(
                metadata=metadata,
                instructions=instructions,
                scripts=scripts,
                resources=resources
            )
        
        except Exception as e:
            logger.error(f"Error parsing skill {skill_dir}: {e}")
            return None
    
    @staticmethod
    def _find_scripts(skill_dir: Path) -> Dict[str, str]:
        """Find executable scripts in skill"""
        scripts = {}
        scripts_dir = skill_dir / "scripts"
        
        if scripts_dir.exists():
            for script_file in scripts_dir.glob("*.py"):
                scripts[script_file.name] = str(script_file)
        
        return scripts
    
    @staticmethod
    def _find_resources(skill_dir: Path) -> Dict[str, str]:
        """Find resource files in skill"""
        resources = {}
        resources_dir = skill_dir / "resources"
        
        if resources_dir.exists():
            for resource_file in resources_dir.rglob("*"):
                if resource_file.is_file():
                    rel_path = resource_file.relative_to(resources_dir)
                    resources[str(rel_path)] = str(resource_file)
        
        return resources


class SkillRegistry:
    """Registry for loaded skills"""
    
    def __init__(self):
        self.skills: Dict[str, SkillContent] = {}
        self.loaded_modules: Dict[str, Any] = {}
    
    def register(self, skill: SkillContent) -> bool:
        """Register a skill"""
        skill_id = skill.metadata.name
        
        if skill_id in self.skills:
            logger.warning(f"Skill {skill_id} already registered, overwriting")
        
        self.skills[skill_id] = skill
        logger.info(f"Registered skill: {skill_id}")
        return True
    
    def get_skill(self, skill_id: str) -> Optional[SkillContent]:
        """Get skill by ID"""
        return self.skills.get(skill_id)
    
    def list_skills(self) -> List[SkillMetadata]:
        """List all registered skills"""
        return [skill.metadata for skill in self.skills.values()]
    
    def find_skills_by_tag(self, tag: str) -> List[SkillContent]:
        """Find skills by tag"""
        return [
            skill for skill in self.skills.values()
            if tag in skill.metadata.tags
        ]
    
    def find_skills_by_keyword(self, keyword: str) -> List[SkillContent]:
        """Find skills by keyword in description"""
        keyword_lower = keyword.lower()
        return [
            skill for skill in self.skills.values()
            if keyword_lower in skill.metadata.description.lower() or
               keyword_lower in skill.metadata.name.lower()
        ]
    
    def load_module(self, skill_id: str, script_name: str) -> Optional[Any]:
        """Load Python module from skill script"""
        skill = self.get_skill(skill_id)
        if not skill:
            logger.error(f"Skill not found: {skill_id}")
            return None
        
        if script_name not in skill.scripts:
            logger.error(f"Script not found: {script_name} in {skill_id}")
            return None
        
        script_path = skill.scripts[script_name]
        module_key = f"{skill_id}/{script_name}"
        
        if module_key in self.loaded_modules:
            return self.loaded_modules[module_key]
        
        try:
            spec = importlib.util.spec_from_file_location(
                module_key,
                script_path
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_key] = module
            spec.loader.exec_module(module)
            
            self.loaded_modules[module_key] = module
            logger.info(f"Loaded module: {module_key}")
            return module
        
        except Exception as e:
            logger.error(f"Error loading module {module_key}: {e}")
            return None


class SkillBot:
    """Wrapper to execute skill as Poe bot"""
    
    def __init__(self, skill: SkillContent, registry: SkillRegistry):
        self.skill = skill
        self.registry = registry
        self.name = skill.metadata.name
        self.description = skill.metadata.description
        self.instructions = skill.metadata.description
    
    async def call_with_instructions(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> str:
        """Execute skill with query"""
        
        # Build execution context
        exec_context = {
            "skill_name": self.skill.metadata.name,
            "query": query,
            "instructions": self.skill.instructions,
            "context": context or {},
        }
        
        # Execute skill instructions
        # In real implementation, this would process the instructions
        # and execute any referenced scripts
        
        result = f"""
# Skill: {self.skill.metadata.name}

**Instructions:**
{self.skill.instructions[:500]}...

**Query:** {query}

**Status:** Ready to execute

**Available Scripts:** {list(self.skill.scripts.keys())}
**Available Resources:** {list(self.skill.resources.keys())}
"""
        
        return result
    
    async def get_skill_actions(self) -> List[str]:
        """Get available actions in skill"""
        actions = []
        
        # List scripts as actions
        for script_name in self.skill.scripts.keys():
            actions.append(f"run-script:{script_name}")
        
        # Parse instructions for action keywords
        if "Task:" in self.skill.instructions:
            actions.append("list-tasks")
        
        return actions


class SkillLoader:
    """Main Skill Loader - orchestrates discovery and registration"""
    
    def __init__(self, skills_root: str = "/home/user/skills"):
        self.skills_root = skills_root
        self.registry = SkillRegistry()
        self.bots: Dict[str, SkillBot] = {}
    
    def load_all_skills(self) -> int:
        """Discover and load all skills"""
        skill_dirs = SkillDiscovery.find_skills(self.skills_root)
        loaded = 0
        
        for skill_dir in skill_dirs:
            skill = SkillDiscovery.parse_skill_file(skill_dir)
            if skill:
                self.registry.register(skill)
                self.bots[skill.metadata.name] = SkillBot(skill, self.registry)
                loaded += 1
        
        logger.info(f"Loaded {loaded} skills")
        return loaded
    
    def load_skill(self, skill_path: str) -> Optional[SkillBot]:
        """Load a specific skill"""
        skill_dir = Path(skill_path)
        
        if not skill_dir.exists():
            logger.error(f"Skill path not found: {skill_path}")
            return None
        
        skill = SkillDiscovery.parse_skill_file(skill_dir)
        if not skill:
            return None
        
        self.registry.register(skill)
        bot = SkillBot(skill, self.registry)
        self.bots[skill.metadata.name] = bot
        
        return bot
    
    def get_bot(self, skill_id: str) -> Optional[SkillBot]:
        """Get bot for skill"""
        return self.bots.get(skill_id)
    
    def list_available_bots(self) -> List[Dict]:
        """List all available bot skills"""
        return [
            {
                "id": skill.metadata.name,
                "description": skill.metadata.description,
                "version": skill.metadata.version,
                "tags": skill.metadata.tags,
                "scripts": list(skill.scripts.keys()),
            }
            for skill in self.registry.list_skills()
        ]
    
    def search_skills(self, query: str) -> List[Dict]:
        """Search for skills"""
        # Try keyword search first
        results = self.registry.find_skills_by_keyword(query)
        
        # If no results, try tag search
        if not results:
            results = self.registry.find_skills_by_tag(query)
        
        return [
            {
                "id": skill.metadata.name,
                "description": skill.metadata.description,
                "tags": skill.metadata.tags,
                "match_type": "keyword" if query.lower() in skill.metadata.description.lower() else "tag"
            }
            for skill in results
        ]


# Global skill loader instance
_skill_loader: Optional[SkillLoader] = None


def get_skill_loader() -> SkillLoader:
    """Get or create global skill loader"""
    global _skill_loader
    if _skill_loader is None:
        _skill_loader = SkillLoader()
    return _skill_loader


async def load_skills() -> int:
    """Load all available skills"""
    loader = get_skill_loader()
    return loader.load_all_skills()


async def get_available_skills() -> List[Dict]:
    """Get list of available skills"""
    loader = get_skill_loader()
    return loader.list_available_bots()


async def search_skills(query: str) -> List[Dict]:
    """Search for skills"""
    loader = get_skill_loader()
    return loader.search_skills(query)


async def execute_skill(skill_id: str, query: str, context: Optional[Dict] = None) -> str:
    """Execute a skill"""
    loader = get_skill_loader()
    bot = loader.get_bot(skill_id)
    
    if not bot:
        return f"Error: Skill '{skill_id}' not found"
    
    try:
        result = await bot.call_with_instructions(query, context)
        return result
    except Exception as e:
        logger.error(f"Error executing skill {skill_id}: {e}")
        return f"Error executing skill: {str(e)}"
