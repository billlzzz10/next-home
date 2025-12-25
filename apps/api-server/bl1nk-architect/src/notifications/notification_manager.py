"""
Notification Manager - Handle Slack, Linear, ClickUp notifications

Manages user notification preferences and routing analysis results 
to registered channels (Slack webhooks, Linear, ClickUp).
"""

import asyncio
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class NotificationChannel(Enum):
    """Supported notification channels"""
    SLACK = "slack"
    LINEAR = "linear"
    CLICKUP = "clickup"


@dataclass
class NotificationPreference:
    """User notification preference"""
    user_id: str
    channel: NotificationChannel
    webhook_url: Optional[str] = None  # For Slack
    api_key: Optional[str] = None      # For Linear/ClickUp
    project_id: Optional[str] = None   # For Linear/ClickUp
    team_id: Optional[str] = None      # For Linear
    enabled: bool = True


class NotificationRegistry:
    """Manages user notification preferences"""
    
    def __init__(self):
        self.preferences: Dict[str, List[NotificationPreference]] = {}
    
    def register_notification(
        self,
        user_id: str,
        channel: NotificationChannel,
        **kwargs
    ) -> NotificationPreference:
        """Register user for notifications"""
        pref = NotificationPreference(user_id=user_id, channel=channel, **kwargs)
        
        if user_id not in self.preferences:
            self.preferences[user_id] = []
        
        self.preferences[user_id].append(pref)
        logger.info(f"Registered {channel.value} notification for user {user_id}")
        return pref
    
    def get_user_preferences(self, user_id: str) -> List[NotificationPreference]:
        """Get all notification preferences for user"""
        return self.preferences.get(user_id, [])
    
    def disable_notification(self, user_id: str, channel: NotificationChannel) -> bool:
        """Disable notification channel for user"""
        if user_id in self.preferences:
            for pref in self.preferences[user_id]:
                if pref.channel == channel:
                    pref.enabled = False
                    return True
        return False


class NotificationManager:
    """Main notification orchestrator"""
    
    def __init__(self):
        self.registry = NotificationRegistry()
        from src.notifications.slack_notifier import SlackNotifier
        from src.notifications.linear_notifier import LinearNotifier
        from src.notifications.clickup_notifier import ClickUpNotifier
        
        self.notifiers = {
            NotificationChannel.SLACK: SlackNotifier(),
            NotificationChannel.LINEAR: LinearNotifier(),
            NotificationChannel.CLICKUP: ClickUpNotifier(),
        }
    
    async def send_analysis_notification(
        self,
        user_id: str,
        analysis_title: str,
        analysis_summary: str,
        analysis_details: Dict,
        task_id: Optional[str] = None,
    ) -> Dict[str, bool]:
        """Send analysis results to all user's registered channels"""
        preferences = self.registry.get_user_preferences(user_id)
        results = {}
        
        tasks = []
        for pref in preferences:
            if not pref.enabled:
                continue
            
            notifier = self.notifiers.get(pref.channel)
            if not notifier:
                logger.warning(f"No notifier for {pref.channel.value}")
                continue
            
            task = notifier.send_notification(
                preference=pref,
                title=analysis_title,
                summary=analysis_summary,
                details=analysis_details,
                task_id=task_id,
            )
            tasks.append((pref.channel.value, task))
        
        for channel_name, task in tasks:
            try:
                success = await task
                results[channel_name] = success
                logger.info(f"✅ Sent to {channel_name}: {success}")
            except Exception as e:
                logger.error(f"❌ Failed to send to {channel_name}: {e}")
                results[channel_name] = False
        
        return results
    
    def register_slack(self, user_id: str, webhook_url: str) -> NotificationPreference:
        """Register Slack webhook for user"""
        return self.registry.register_notification(
            user_id=user_id,
            channel=NotificationChannel.SLACK,
            webhook_url=webhook_url,
        )
    
    def register_linear(
        self,
        user_id: str,
        api_key: str,
        team_id: str,
        project_id: Optional[str] = None,
    ) -> NotificationPreference:
        """Register Linear API for user"""
        return self.registry.register_notification(
            user_id=user_id,
            channel=NotificationChannel.LINEAR,
            api_key=api_key,
            team_id=team_id,
            project_id=project_id,
        )
    
    def register_clickup(
        self,
        user_id: str,
        api_key: str,
        project_id: str,
    ) -> NotificationPreference:
        """Register ClickUp API for user"""
        return self.registry.register_notification(
            user_id=user_id,
            channel=NotificationChannel.CLICKUP,
            api_key=api_key,
            project_id=project_id,
        )


_notification_manager: Optional[NotificationManager] = None


def get_notification_manager() -> NotificationManager:
    """Get or create notification manager"""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager
