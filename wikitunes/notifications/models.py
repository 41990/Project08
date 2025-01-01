from django.db import models
from django.utils import timezone

from accounts.models import Account

class Notification(models.Model):
    """
    Represents a notification sent to a user or account.
    """
    NOTIFICATION_TYPES = [
        ('message', 'Message'),
        ('alert', 'Alert'),
        ('reminder', 'Reminder'),
        # Add more types as needed
    ]
    
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, help_text="User receiving the notification.")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, help_text="Type of notification.")
    content = models.TextField(help_text="The content of the notification.")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Time when the notification was sent.")
    read = models.BooleanField(default=False, help_text="Whether the notification has been read.")
    
    def __str__(self):
        return f"Notification to {self.recipient.username} at {self.timestamp}"

class NotificationLog(models.Model):
    """
    Stores logs of user interactions with notifications.
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="logs")
    user = models.ForeignKey(Account, on_delete=models.CASCADE, help_text="User who interacted with the notification.")
    action = models.CharField(max_length=20, choices=[('read', 'Read'), ('dismissed', 'Dismissed')], help_text="Action performed on the notification.")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Time when the action was performed.")
    
    def __str__(self):
        return f"Notification log for {self.user.username} on {self.notification.content} at {self.timestamp}"

