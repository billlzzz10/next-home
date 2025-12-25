"""
Orchestrator v2 - 8-step workflow with notifications

Controls the complete architecture analysis workflow with:
- Notifications to Slack, Linear, ClickUp
- Beautiful widget-based reporting
- Task ID linking
"""

import asyncio
import logging
from typing import AsyncGenerator, Optional

from src.github_client import GitHubClient
from src.gemini_client import deep_research_task
from src.auth import get_installation_id, get_access_token
from src.notifications import get_notification_manager
from src.widgets import create_analysis_report
from utils.formatter import format_architecture_plan

logger = logging.getLogger(__name__)


async def run_architect_workflow_v2(
    user_query: str,
    user_id: str,
    task_id: Optional[str] = None,
) -> AsyncGenerator[str, None]:
    """
    Execute complete 8-step architecture analysis workflow with notifications.
    
    Yields streaming text chunks as workflow progresses.
    
    Args:
        user_query: User's request/question
        user_id: Poe user ID for authentication
        task_id: Optional Linear/ClickUp task ID
        
    Yields:
        Markdown-formatted text chunks for streaming to user
    """
    
    try:
        # Step 0: Get GitHub credentials
        installation_id = get_installation_id(user_id)
        access_token = get_access_token(user_id)
        
        if not installation_id or not access_token:
            yield "❌ GitHub authentication failed. Please re-authenticate."
            return
        
        # Initialize GitHub client
        gh_client = GitHubClient(installation_id, access_token)
        
        # Analysis context
        analysis_data = {
            "repository": "",
            "files": [],
            "files_count": 0,
            "python_deps": [],
            "typescript_deps": [],
            "duplicates": [],
        }
        
        # STEP 1: Scan Repository Structure
        yield "## Step 1: Repository Structure Scan\n\n"
        yield "🔍 Analyzing repository structure...\n\n"
        
        try:
            repos = await gh_client.list_repositories(limit=5)
            if not repos:
                yield "❌ No repositories found. Please install Bl1nk on a repository.\n"
                return
            
            repo = repos[0]
            analysis_data["repository"] = repo['name']
            
            yield f"📦 Repository: `{repo['name']}`\n"
            yield f"Description: {repo.get('description', 'N/A')}\n"
            yield f"Language: {repo.get('language', 'N/A')}\n\n"
            
            files = await gh_client.list_files(repo['name'], limit=50)
            analysis_data["files"] = files
            analysis_data["files_count"] = len(files)
            
            yield f"📁 Found {len(files)} files\n\n"
            
        except Exception as e:
            logger.exception(f"Step 1 error: {e}")
            yield f"⚠️ Warning in step 1: {str(e)}\n\n"
        
        # STEP 2: Analyze Dependencies
        yield "## Step 2: Dependency Analysis\n\n"
        yield "📚 Analyzing dependencies...\n\n"
        
        try:
            py_deps = await gh_client.get_python_dependencies(repo['name'])
            ts_deps = await gh_client.get_typescript_dependencies(repo['name'])
            
            analysis_data["python_deps"] = py_deps or []
            analysis_data["typescript_deps"] = ts_deps or []
            
            if py_deps:
                yield f"🐍 Python dependencies: {len(py_deps)} found\n"
                for dep in py_deps[:5]:
                    yield f"  - {dep}\n"
                if len(py_deps) > 5:
                    yield f"  ... and {len(py_deps) - 5} more\n"
            
            if ts_deps:
                yield f"\n📘 TypeScript dependencies: {len(ts_deps)} found\n"
                for dep in ts_deps[:5]:
                    yield f"  - {dep}\n"
                if len(ts_deps) > 5:
                    yield f"  ... and {len(ts_deps) - 5} more\n"
            
            yield "\n"
            
        except Exception as e:
            logger.exception(f"Step 2 error: {e}")
            yield f"⚠️ Warning in step 2: {str(e)}\n\n"
        
        # STEP 3: Detect Code Duplication
        yield "## Step 3: Code Duplication Detection\n\n"
        yield "🔎 Scanning for duplicate code patterns...\n\n"
        
        try:
            duplicates = await gh_client.detect_code_duplicates(repo['name'])
            analysis_data["duplicates"] = duplicates or []
            
            if duplicates:
                yield f"⚠️ Found {len(duplicates)} duplicate patterns:\n\n"
                for dup in duplicates[:3]:
                    yield f"- **{dup['pattern']}** (found {dup['count']} times)\n"
                if len(duplicates) > 3:
                    yield f"- ... and {len(duplicates) - 3} more patterns\n"
            else:
                yield "✅ No significant code duplicates found\n"
            
            yield "\n"
            
        except Exception as e:
            logger.exception(f"Step 3 error: {e}")
            yield f"⚠️ Warning in step 3: {str(e)}\n\n"
        
        # STEPS 4-8: Call Gemini Deep Research
        yield "## Steps 4-8: Comprehensive Analysis\n\n"
        yield "🧠 Running AI-powered deep research...\n"
        yield "_This may take a minute. Processing..._\n\n"
        
        try:
            context = {
                "user_query": user_query,
                "repository": repo.get("name", "unknown"),
                "files_count": len(files),
                "file_samples": files[:10],
                "python_deps": py_deps[:10] if py_deps else [],
                "typescript_deps": ts_deps[:10] if ts_deps else [],
                "duplicates": duplicates[:5] if duplicates else [],
            }
            
            research_result = await deep_research_task(
                query=user_query,
                context=context
            )
            
            if research_result:
                yield research_result
            else:
                yield "⚠️ Deep research completed but returned no results\n"
            
        except Exception as e:
            logger.exception(f"Gemini research error: {e}")
            yield f"⚠️ Deep research error: {str(e)}\n"
            yield "Creating fallback analysis...\n\n"
            
            yield await create_fallback_plan(repo, files, py_deps, ts_deps)
        
        # Final summary
        yield "\n\n## Analysis Summary\n\n"
        yield "✅ **Workflow Complete**\n\n"
        
        # Create widget-based report
        yield create_analysis_report(
            title=f"Analysis: {repo.get('name', 'Repository')}",
            repository=repo.get('name', 'unknown'),
            files_count=len(files),
            duplicates=duplicates or [],
            python_deps=py_deps or [],
            typescript_deps=ts_deps or [],
        )
        
        # Send notifications
        yield "\n\n## 📤 Sending Notifications\n\n"
        notification_manager = get_notification_manager()
        
        results = await notification_manager.send_analysis_notification(
            user_id=user_id,
            analysis_title=f"Architecture Analysis: {repo.get('name')}",
            analysis_summary=f"Analysis of {len(files)} files with {len(py_deps or []) + len(ts_deps or [])} dependencies",
            analysis_details=analysis_data,
            task_id=task_id,
        )
        
        for channel, success in results.items():
            status = "✅" if success else "❌"
            yield f"{status} {channel.upper()}\n"
        
        yield "\nNext steps:\n"
        yield "1. Review the recommendations above\n"
        yield "2. Create issues for priority items\n"
        yield "3. Start with consolidation tasks\n"
        yield "4. Update team documentation\n"
        
    except Exception as e:
        logger.exception(f"Workflow error: {e}")
        yield f"\n\n❌ **Workflow Error**: {str(e)}\n"


async def create_fallback_plan(repo, files, py_deps, ts_deps):
    """Create basic fallback plan if Gemini fails"""
    
    plan = "\n## Fallback Architecture Plan\n\n"
    plan += "| Task | Description | Priority |\n"
    plan += "|------|-------------|----------|\n"
    
    tasks = [
        ("1. Consolidate", "Consolidate duplicate code patterns", "High"),
        ("2. Dependencies", "Update and audit dependencies", "High"),
        ("3. Testing", "Improve test coverage", "Medium"),
        ("4. Documentation", "Update technical documentation", "Medium"),
        ("5. CI/CD", "Set up automated pipelines", "Medium"),
        ("6. Docker", "Create optimized Docker images", "Low"),
        ("7. Linting", "Configure code quality checks", "Low"),
        ("8. Monitoring", "Add monitoring and logging", "Low"),
    ]
    
    for task, desc, priority in tasks:
        plan += f"| {task} | {desc} | {priority} |\n"
    
    return plan
