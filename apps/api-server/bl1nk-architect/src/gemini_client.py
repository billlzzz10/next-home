"""
Gemini Deep Research Client

Wrapper for Google Gemini Deep Research API.
Handles background task polling and result parsing.
"""

import os
import asyncio
import logging
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


async def deep_research_task(
    query: str,
    context: Optional[Dict[str, Any]] = None
) -> str:
    """
    Execute a Gemini Deep Research task with polling.
    
    Args:
        query: Main research question
        context: Additional context (repository info, dependencies, etc.)
        
    Returns:
        Research results as formatted markdown string
    """
    
    try:
        from google import genai
    except ImportError:
        logger.error("google-genai not installed")
        return "❌ Gemini API not available. Please install google-genai"
    
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "❌ GOOGLE_API_KEY environment variable not set"
        
        client = genai.Client(api_key=api_key)
        
        # Build research prompt
        prompt = build_research_prompt(query, context)
        
        logger.info("Starting Gemini Deep Research task...")
        
        # Create interaction with background=True
        try:
            interaction = client.interactions.create(
                input=prompt,
                agent="deep-research-pro-preview-12-2025",
                background=True
            )
            
            interaction_id = interaction.id
            logger.info(f"Research task started: {interaction_id}")
            
        except Exception as e:
            logger.exception(f"Failed to create research task: {e}")
            return f"❌ Failed to start research: {str(e)}"
        
        # Poll for completion
        max_polls = 120  # 10 minutes with 5-second intervals
        poll_count = 0
        
        while poll_count < max_polls:
            await asyncio.sleep(5)  # Poll every 5 seconds
            poll_count += 1
            
            try:
                status_check = client.interactions.get(interaction_id)
                
                if status_check.status == "completed":
                    logger.info(f"Research completed after {poll_count} polls")
                    
                    # Extract result
                    if hasattr(status_check, 'outputs') and status_check.outputs:
                        result_text = status_check.outputs[-1].text if hasattr(status_check.outputs[-1], 'text') else str(status_check.outputs[-1])
                        return format_research_output(result_text)
                    else:
                        return "⚠️ Research completed but no output found"
                
                elif status_check.status == "failed":
                    error_msg = getattr(status_check, 'error', 'Unknown error')
                    logger.error(f"Research failed: {error_msg}")
                    return f"❌ Research failed: {error_msg}"
                
                elif status_check.status == "processing":
                    if poll_count % 12 == 0:  # Log every minute
                        logger.info(f"Research still processing... ({poll_count * 5}s elapsed)")
                
            except Exception as e:
                logger.exception(f"Error checking research status: {e}")
                # Continue polling, might be temporary
        
        logger.error(f"Research task timed out after {max_polls * 5} seconds")
        return "⏱️ Research task timed out. Please try again."
        
    except Exception as e:
        logger.exception(f"Deep research error: {e}")
        return f"❌ Research error: {str(e)}"


def build_research_prompt(query: str, context: Optional[Dict] = None) -> str:
    """Build comprehensive research prompt with context"""
    
    prompt = f"""You are an expert software architect analyzing a GitHub repository.

PRIMARY QUESTION:
{query}

"""
    
    if context:
        if context.get("repository"):
            prompt += f"Repository: {context['repository']}\n"
        if context.get("files_count"):
            prompt += f"Files analyzed: {context['files_count']}\n"
        
        if context.get("python_deps"):
            prompt += f"\nPython Dependencies:\n"
            for dep in context["python_deps"][:5]:
                prompt += f"- {dep}\n"
        
        if context.get("typescript_deps"):
            prompt += f"\nTypeScript Dependencies:\n"
            for dep in context["typescript_deps"][:5]:
                prompt += f"- {dep}\n"
    
    prompt += """

ANALYSIS FRAMEWORK:
1. **Code Organization**: Evaluate the repository structure and organization
2. **Dependency Management**: Review dependencies for duplicates and outdated packages
3. **Code Quality**: Identify duplication patterns and quality issues
4. **Consolidation Plan**: Provide specific steps to improve the codebase
5. **Testing Strategy**: Recommend testing improvements
6. **Docker Strategy**: Suggest Docker optimization
7. **Linting & Quality**: Recommend linting tools and configurations
8. **Documentation**: Suggest documentation improvements

FORMAT YOUR RESPONSE AS:
## Analysis Results

### 1. Code Organization
[Analysis]

### 2. Dependency Management
[Analysis]

### 3. Code Quality Issues
[Analysis with specific examples]

### 4. Consolidation Plan
- Task: [specific action]
- Priority: [High/Medium/Low]
- Effort: [days]
- Impact: [description]

### 5. Testing Recommendations
[Specific recommendations]

### 6. Docker & Deployment
[Specific recommendations]

### 7. Linting & Code Quality
[Tools and configuration]

### 8. Documentation
[Specific recommendations]

## Summary
- Total Effort: [estimate in days]
- Top 3 Priorities:
  1. [priority]
  2. [priority]
  3. [priority]
"""
    
    return prompt


def format_research_output(raw_output: str) -> str:
    """Format Gemini research output for streaming to user"""
    
    # Clean up output
    output = raw_output.strip()
    
    # Ensure markdown formatting
    if not output.startswith("#"):
        output = f"## Research Results\n\n{output}"
    
    # Add emojis for better formatting
    output = output.replace("### 1.", "### 1️⃣")
    output = output.replace("### 2.", "### 2️⃣")
    output = output.replace("### 3.", "### 3️⃣")
    output = output.replace("### 4.", "### 4️⃣")
    output = output.replace("### 5.", "### 5️⃣")
    output = output.replace("### 6.", "### 6️⃣")
    output = output.replace("### 7.", "### 7️⃣")
    output = output.replace("### 8.", "### 8️⃣")
    
    return output


async def parse_research_results(raw_json: str) -> Dict[str, Any]:
    """Parse structured research results (if API returns JSON)"""
    
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        logger.warning("Could not parse research results as JSON")
        return {
            "raw": raw_json,
            "parsed": False
        }
