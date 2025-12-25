"""
Introduction Message Manager

Handles customizable introduction messages for the bot.
Provides friendly welcome messages to users.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class IntroductionManager:
    """Manages bot introduction and welcome messages"""
    
    @staticmethod
    def get_introduction_message() -> str:
        """
        Get the introduction message for Bl1nk Architect.
        
        Returns:
            Markdown-formatted introduction message
        """
        return """🏗️ **Welcome to Bl1nk Architect**

I'm an AI-powered GitHub repository architecture analyzer. I help you understand, analyze, and improve your codebase structure.

## What I Do

• **Scan your repository** - Analyze files, dependencies, and code structure
• **Identify issues** - Detect duplications, outdated packages, code quality problems
• **Generate plans** - Create actionable 8-step refactoring plans
• **Deep research** - Use Gemini AI for comprehensive architecture analysis
• **Export reports** - Download analysis as Markdown, JSON, or CSV files

## How to Use Me

Simply send me:
- "Analyze my repo" - Start a full architecture analysis
- "Check dependencies" - Review Python and TypeScript packages
- "Find duplicates" - Detect code duplication patterns
- "Generate plan" - Create a refactoring roadmap

## Features

✨ **GitHub Integration** - Direct repository access
✨ **AI Analysis** - Powered by Gemini Deep Research
✨ **Multiple Formats** - Export reports as .md, .json, .csv
✨ **8-Step Workflow** - Comprehensive architecture review
✨ **Real-time Streaming** - See results as they're generated

## First Steps

1. **Authenticate** - Click the GitHub link to authorize access
2. **Provide query** - Ask about your repository
3. **Wait for analysis** - Deep research is running
4. **Download report** - Get your architecture analysis

---

Ready to analyze your architecture? Just ask! 🚀"""
    
    @staticmethod
    def get_custom_introduction(
        repo_name: Optional[str] = None,
        user_name: Optional[str] = None
    ) -> str:
        """
        Get personalized introduction message.
        
        Args:
            repo_name: Repository name to mention
            user_name: User name to personalize with
            
        Returns:
            Personalized introduction message
        """
        intro = "🏗️ **Welcome"
        
        if user_name:
            intro += f", {user_name}!"
        else:
            intro += " to Bl1nk Architect**"
        
        intro += """

I analyze GitHub repositories to create architecture improvement plans.

**Getting Started:**
"""
        
        if repo_name:
            intro += f"\n✓ Found repository: **{repo_name}**"
            intro += "\n✓ Ready to analyze?"
        else:
            intro += "\n1. Authorize GitHub access"
            intro += "\n2. Ask me to analyze your repository"
            intro += "\n3. I'll create a detailed architecture plan"
        
        intro += """

What would you like me to analyze?"""
        
        return intro
    
    @staticmethod
    def get_error_introduction() -> str:
        """Get introduction message when authentication needed"""
        return """🔒 **Bl1nk Architect - Authentication Required**

To analyze your GitHub repositories, I need access to your code.

**Next Steps:**
1. Click the authorization link below
2. Install the Bl1nk Architect GitHub App
3. Select repositories to analyze
4. Come back and ask me to analyze!

Once authorized, I can:
• Scan your repository structure
• Analyze dependencies
• Detect code duplications
• Generate 8-step refactoring plans
• Export reports as files

[Authorize GitHub Access]

After authorization, you'll see personalized analysis options! 🚀"""
    
    @staticmethod
    def get_onboarding_steps() -> str:
        """Get onboarding instructions"""
        return """📚 **Onboarding Guide**

### Step 1: Authorization ✓
Click the GitHub link to grant access to your repositories.

### Step 2: Choose Repository ✓
Select which repositories to analyze.

### Step 3: Send Query ✓
Ask me to analyze:
- "Analyze my repo"
- "Check code quality"
- "Find vulnerabilities"
- "Create refactoring plan"

### Step 4: Get Analysis ✓
I'll generate:
- Architecture insights
- Dependency analysis
- Code quality report
- Refactoring recommendations
- Downloadable files

### Step 5: Download Report ✓
Get your analysis as:
- Markdown (.md)
- JSON (.json)
- CSV (.csv)

**Ready?** Start by asking me to analyze your repository! 🚀"""


class IntroductionMessages:
    """Pre-defined introduction messages for different scenarios"""
    
    MAIN = IntroductionManager.get_introduction_message()
    
    AUTHENTICATED = """🏗️ **Bl1nk Architect Ready**

Your GitHub account is connected! What would you like me to analyze?

**Quick Commands:**
• "Analyze my repositories"
• "Check code quality"
• "Find code duplicates"
• "Create architecture plan"
• "Audit dependencies"

Send a message to get started! 🚀"""
    
    WAITING_AUTH = IntroductionManager.get_error_introduction()
    
    ANALYSIS_MODE = """🔍 **Analysis Mode Activated**

I'm analyzing your repository structure, dependencies, and code quality.

This typically takes 1-2 minutes for comprehensive analysis.

Please stand by... ⏳"""
    
    HELP_MESSAGE = """📖 **How to Use Bl1nk Architect**

### Main Features

**1. Repository Analysis**
```
Query: "Analyze my repository"
Output: Full architecture assessment
```

**2. Dependency Audit**
```
Query: "Check my dependencies"
Output: Python and TypeScript package analysis
```

**3. Code Quality**
```
Query: "Check code quality"
Output: Duplication detection and quality metrics
```

**4. Architecture Plan**
```
Query: "Create refactoring plan"
Output: 8-step improvement roadmap
```

**5. Export Reports**
```
Output: Download as .md, .json, or .csv
```

### Advanced Features

• GitHub App integration for private repos
• Gemini AI-powered deep research
• Real-time streaming analysis
• Multi-format report export
• Security scanning
• Dependency vulnerability detection

### Support

Having issues? Try:
1. Re-authorize your GitHub account
2. Make sure you have access to the repository
3. Check that the repository isn't too large (>10GB)

Need more help? 📧"""
