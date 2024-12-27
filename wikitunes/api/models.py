from django.db import models
from django.utils import timezone

from ..accounts.models import CustomUser

class APIRequest(models.Model):
    """
    Stores information about an API request.
    """
    endpoint = models.CharField(max_length=255, help_text="The API endpoint accessed.")
    method = models.CharField(
        max_length=10, 
        choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], 
        help_text="HTTP Method."
    )
    request_body = models.JSONField(blank=True, null=True, help_text="Request body (if any).")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Timestamp of the request.")
    user_ip = models.GenericIPAddressField(blank=True, null=True, help_text="IP address of the user making the request.")
    status_code = models.IntegerField(help_text="HTTP status code returned by the API.")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.method} {self.endpoint} at {self.timestamp}"

class APIResponse(models.Model):
    """
    Stores information about an API response.
    """
    request = models.ForeignKey(APIRequest, on_delete=models.CASCADE, related_name="responses")
    response_body = models.JSONField(help_text="Response body returned by the API.")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Timestamp of the response.")
    status_code = models.IntegerField(help_text="HTTP status code of the response.")
    
    def __str__(self):
        return f"Response to {self.request.endpoint} at {self.timestamp}"

class APIKey(models.Model):
    """
    Stores API keys and associated metadata for access control.
    """
    key = models.CharField(max_length=64, unique=True, help_text="Unique API key.")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="User associated with the API key.")
    created_at = models.DateTimeField(default=timezone.now, help_text="Timestamp when the API key was created.")
    expired_at = models.DateTimeField(blank=True, null=True, help_text="Timestamp when the API key will expire.")
    is_active = models.BooleanField(default=True, help_text="Whether the API key is active.")
    
    def __str__(self):
        return f"API Key for {self.user.username}"

