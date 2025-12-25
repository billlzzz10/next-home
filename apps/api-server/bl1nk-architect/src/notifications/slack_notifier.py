"""
Slack Webhook Notifier

Sends analysis notifications to Slack channels via webhooks.
"""

import httpx
import logging
import json
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class SlackNotifier:
    """Send notifications via Slack webhooks"""
    
    async def send_notification(
        self,
        preference,
        title: str,
        summary: str,
        details: Dict,
        task_id: Optional[str] = None,
    ) -> bool:
        """
        Send notification to Slack channel
        
        Args:
            preference: NotificationPreference with webhook_url
            title: Analysis title
            summary: Summary text
            details: Analysis details dict
            task_id: Optional task ID
            
        Returns:
            True if successful, False otherwise
        """
        if not preference.webhook_url:
            logger.warning("No Slack webhook URL configured")
            return False
        
        try:
            payload = self._build_slack_payload(
                title, summary, details, task_id
            )
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    preference.webhook_url,
                    json=payload,
                    timeout=10.0,
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ Slack notification sent successfully")
                    return True
                else:
                    logger.error(
                        f"Slack API error: {response.status_code} - {response.text}"
                    )
                    return False
                    
        except Exception as e:
            logger.error(f"Slack notification error: {e}")
            return False
    
    def _build_slack_payload(
        self,
        title: str,
        summary: str,
        details: Dict,
        task_id: Optional[str] = None,
    ) -> Dict:
        """Build Slack message payload"""
        
        fields = []
        
        if details.get("repository"):
            fields.append({
                "title": "Repository",
                "value": details["repository"],
                "short": True
            })
        
        if details.get("files_count"):
            fields.append({
                "title": "Files Analyzed",
                "value": str(details["files_count"]),
                "short": True
            })
        
        if details.get("duplicates"):
            fields.append({
                "title": "Code Duplicates",
                "value": f"{len(details['duplicates'])} patterns found",
                "short": True
            })
        
        if details.get("python_deps"):
            fields.append({
                "title": "Python Dependencies",
                "value": str(len(details["python_deps"])),
                "short": True
            })
        
        if details.get("typescript_deps"):
            fields.append({
                "title": "TypeScript Dependencies",
                "value": str(len(details["typescript_deps"])),
                "short": True
            })
        
        payload = {
            "attachments": [
                {
                    "fallback": title,
                    "color": "#2E7D32",
                    "title": f"🏗️ {title}",
                    "text": summary,
                    "fields": fields,
                    "footer": "Bl1nk Architect Analysis",
                    "ts": int(__import__('time').time()),
                }
            ]
        }
        
        if task_id:
            payload["attachments"][0]["text"] += f"\n\n📋 Task ID: `{task_id}`"
        
        return payload
