from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from content.models import Post
from forums.models import Forum
from research.models import Blog, Event, Article

class  BaseAnalyticsModel(models.Model):
    """
    Base model for analytics models.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Associated post."
    )
    
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        null=True,   
        blank=True,
        help_text="Associated blog."
    )
    
    forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Associated forum."
    )
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Associated event."
    )
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Associated article."
    )
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Associated user."
    )
    
    pub_date = models.DateTimeField(auto_now=True, help_text="Date when the analytics data was published.")
    
    class Meta:
        abstract = True


class Repost(BaseAnalyticsModel):
    """
    Represents the reposts of a post.
    """
    
    def __str__(self):
        return f"Reposts: {self.count}"


class Like(BaseAnalyticsModel):
    """
    Represents the likes of a post.
    """
    type = models.CharField(max_length=20, help_text="Type of like (e.g., thumbs up, heart, etc.).")    
    
    def __str__(self):
        return f"Likes: {self.count}"
    
    
class Share(BaseAnalyticsModel):
    """
    Represents the shares of a post.
    """
    where = models.CharField(max_length=50, help_text="Where the post was shared (e.g., social media platform).")
    
    def __str__(self):
        return f"Shares: {self.count}"

class View(BaseAnalyticsModel):
    """
    Represents the views of a post.
    """
    device_type = models.CharField(max_length=50, help_text="Type of device used to view the post.")
    os = models.CharField(max_length=50, help_text="Operating system of the device.")
    browser = models.CharField(max_length=50, help_text="Browser used to view the post.")
    ip_address = models.GenericIPAddressField(help_text="IP address of the device.")
    
    def __str__(self):
        return f"Views: {self.count}"