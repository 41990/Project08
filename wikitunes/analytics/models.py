from django.db import models
from django.utils import timezone

from accounts.models import CustomUser

class Event(models.Model):
    """
    Represents an event (e.g., user actions, clicks, or other interactions).
    """
    EVENT_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('click', 'Click'),
        ('view', 'View'),
        ('submit', 'Submit'),
        ('upload', 'Upload'),
        ('download', 'Download')
        # Add more events as needed
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="User who triggered the event.")
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES, help_text="Type of event.")
    timestamp = models.DateTimeField(default=timezone.now, help_text="When the event occurred.")
    metadata = models.JSONField(blank=True, null=True, help_text="Additional data associated with the event (e.g., button clicked).")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Event {self.event_type} by {self.user.username} at {self.timestamp}"

class UserSession(models.Model):
    """
    Represents a session of a user on the platform.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="User associated with the session.")
    session_start = models.DateTimeField(default=timezone.now, help_text="Session start time.")
    session_end = models.DateTimeField(null=True, blank=True, help_text="Session end time.")
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="IP address from which the session originated.")
    
    def __str__(self):
        return f"Session for {self.user.username} from {self.session_start} to {self.session_end}"

class PageView(models.Model):
    """
    Tracks views of pages on the platform.
    """
    page_url = models.URLField(help_text="The URL of the page that was viewed.")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="User who viewed the page.")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Time when the page was viewed.")
    session = models.ForeignKey(UserSession, null=True, blank=True, on_delete=models.CASCADE, help_text="Session during which the page was viewed.")
    
    def __str__(self):
        return f"Page view of {self.page_url} by {self.user.username} at {self.timestamp}"
