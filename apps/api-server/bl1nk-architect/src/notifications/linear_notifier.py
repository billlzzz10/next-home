"""
Linear API Notifier

Creates or updates Linear issues with analysis results.
Links to task IDs if provided.
"""

import httpx
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class LinearNotifier:
    """Send notifications via Linear API"""
    
    BASE_URL = "https://api.linear.app/graphql"
    
    async def send_notification(
        self,
        preference,
        title: str,
        summary: str,
        details: Dict,
        task_id: Optional[str] = None,
    ) -> bool:
        """
        Create or update Linear issue with analysis
        
        Args:
            preference: NotificationPreference with api_key, team_id, project_id
            title: Analysis title
            summary: Summary text
            details: Analysis details dict
            task_id: Optional task ID to link
            
        Returns:
            True if successful, False otherwise
        """
        if not preference.api_key or not preference.team_id:
            logger.warning("Missing Linear API key or team_id")
            return False
        
        try:
            issue_data = self._build_linear_issue(
                title, summary, details, task_id
            )
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.BASE_URL,
                    json={"query": issue_data["mutation"]},
                    headers={
                        "Authorization": f"Bearer {preference.api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout=10.0,
                )
                
                result = response.json()
                
                if "errors" in result:
                    logger.error(f"Linear API error: {result['errors']}")
                    return False
                
                if "data" in result and result["data"].get("issueCreate"):
                    issue_id = result["data"]["issueCreate"]["issue"]["id"]
                    logger.info(f"✅ Linear issue created: {issue_id}")
                    return True
                
                return False
                    
        except Exception as e:
            logger.error(f"Linear notification error: {e}")
            return False
    
    def _build_linear_issue(
        self,
        title: str,
        summary: str,
        details: Dict,
        task_id: Optional[str] = None,
    ) -> Dict:
        """Build Linear GraphQL mutation for creating issue"""
        
        description_lines = [
            summary,
            "",
            "## Analysis Details",
        ]
        
        if details.get("repository"):
            description_lines.append(f"**Repository**: {details['repository']}")
        
        if details.get("files_count"):
            description_lines.append(f"**Files Analyzed**: {details['files_count']}")
        
        if details.get("duplicates"):
            description_lines.append(
                f"**Code Duplicates**: {len(details['duplicates'])} patterns"
            )
        
        if details.get("python_deps"):
            description_lines.append(
                f"**Python Dependencies**: {len(details['python_deps'])}"
            )
        
        if details.get("typescript_deps"):
            description_lines.append(
                f"**TypeScript Dependencies**: {len(details['typescript_deps'])}"
            )
        
        if task_id:
            description_lines.append(f"\n**Task ID**: `{task_id}`")
        
        description = "\n".join(description_lines)
        
        mutation = f'''
        mutation {{
          issueCreate(
            input: {{
              title: "{title}"
              description: "{description}"
              teamId: "{details.get('team_id', '')}"
              projectId: "{details.get('project_id', '')}"
            }}
          ) {{
            issue {{
              id
              identifier
              title
            }}
          }}
        }}
        '''
        
        return {"mutation": mutation}
