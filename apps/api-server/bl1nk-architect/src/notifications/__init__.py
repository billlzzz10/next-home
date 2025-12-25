"""Notification system package"""

from src.notifications.notification_manager import (
    NotificationManager,
    NotificationChannel,
    NotificationPreference,
    get_notification_manager,
)

__all__ = [
    "NotificationManager",
    "NotificationChannel",
    "NotificationPreference",
    "get_notification_manager",
]
