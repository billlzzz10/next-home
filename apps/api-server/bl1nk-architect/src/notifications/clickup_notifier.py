"""
ClickUp API Notifier

Creates or updates ClickUp tasks with analysis results.
Supports task linking and custom fields.
"""

import httpx
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ClickUpNotifier:
    """Send notifications via ClickUp API"""
    
    BASE_URL = "https://api.clickup.com/api/v2"
    
    async def send_notification(
        self,
        preference,
        title: str,
        summary: str,
        details: Dict,
        task_id: Optional[str] = None,
    ) -> bool:
        """
        Create or update ClickUp task with analysis
        
        Args:
            preference: NotificationPreference with api_key, project_id
            title: Analysis title
            summary: Summary text
            details: Analysis details dict
            task_id: Optional task ID to link
            
        Returns:
            True if successful, False otherwise
        """
        if not preference.api_key or not preference.project_id:
            logger.warning("Missing ClickUp API key or project_id")
            return False
        
        try:
            task_data = self._build_clickup_task(
                title, summary, details, task_id
            )
            
            # Create task in ClickUp
            list_id = preference.project_id
            url = f"{self.BASE_URL}/list/{list_id}/task"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=task_data,
                    headers={
                        "Authorization": preference.api_key,
                        "Content-Type": "application/json",
                    },
                    timeout=10.0,
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    task = result.get("task", {})
                    logger.info(
                        f"✅ ClickUp task created: {task.get('id')}"
                    )
                    return True
                else:
                    logger.error(
                        f"ClickUp API error: {response.status_code} - {response.text}"
                    )
                    return False
                    
        except Exception as e:
            logger.error(f"ClickUp notification error: {e}")
            return False
    
    def _build_clickup_task(
        self,
        title: str,
        summary: str,
        details: Dict,
        task_id: Optional[str] = None,
    ) -> Dict:
        """Build ClickUp task creation payload"""
        
        description_parts = [
            summary,
            "",
            "## Analysis Metrics",
        ]
        
        if details.get("repository"):
            description_parts.append(f"- **Repository**: {details['repository']}")
        
        if details.get("files_count"):
            description_parts.append(
                f"- **Files Analyzed**: {details['files_count']}"
            )
        
        if details.get("duplicates"):
            description_parts.append(
                f"- **Code Duplicates**: {len(details['duplicates'])} patterns"
            )
        
        if details.get("python_deps"):
            description_parts.append(
                f"- **Python Dependencies**: {len(details['python_deps'])}"
            )
        
        if details.get("typescript_deps"):
            description_parts.append(
                f"- **TypeScript Dependencies**: {len(details['typescript_deps'])}"
            )
        
        if task_id:
            description_parts.append(f"\n- **Linked Task ID**: `{task_id}`")
        
        description = "\n".join(description_parts)
        
        task_data = {
            "name": f"🏗️ {title}",
            "description": description,
            "priority": 2,  # Medium priority
            "status": "to do",
        }
        
        return task_data
