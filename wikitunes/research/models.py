from django.db import models
from ..locations.models import Location
from ..accounts.models import Account, CustomUser
from ..forums.models import forum_data_desc_dir_path
from ..tunes.models import BaseModel, SiteReaction


class Event(BaseModel, SiteReaction):
    """
    Represents an event.
    """
    reaction_field = 'comment'
    comment_field = 'parent_comment'
    
    title = models.CharField(max_length=100, help_text="Title of the event.")
    description = models.FileField(upload_to=forum_data_desc_dir_path, help_text="File describing the event content.")
    owners = models.ManyToManyField('Account', related_name='events')
    start_time = models.DateTimeField(help_text="Event start time.")
    end_time = models.DateTimeField(help_text="Event end time.")
    media = models.ForeignKey(
        'Media',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Media associated with the event."
    )

    def __str__(self):
        return self.title
    
    
class SearchHistory(models.Model):
    SEARCH_CATEGORIES = [
        ('general', 'General'),
        ('forum', 'Forum'),
        ('post', 'Post'),
        ('event', 'Event'),
        ('article', 'Article'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('document', 'Document'),
    ]

    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        help_text="The user who performed the search."
    )
    search_term = models.CharField(max_length=255, help_text="The search term entered by the user.")
    category = models.CharField(
        max_length=20, 
        choices=SEARCH_CATEGORIES, 
        default='general', 
        help_text="Category of the search."
    )
    date = models.DateTimeField(auto_now_add=True, help_text="The date and time of the search.")
    results_count = models.IntegerField(default=0, help_text="Number of results returned for the search.")
    device_type = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        help_text="Type of device used for the search."
    )
    os = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        help_text="Operating system of the device."
    )
    browser = models.CharField(
        max_length=50, 
        null=True,
        blank=True, 
        help_text="Browser used for the search."
    )
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True, 
        help_text="IP address at the time of the search."
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Location associated with the search event."
    )
    search_duration = models.DurationField(
        null=True, 
        blank=True, 
        help_text="Time taken to complete the search."
    )
    clicked_result = models.TextField(
        null=True, 
        blank=True, 
        help_text="Details of the result clicked by the user."
    )
    search_engine = models.CharField(
        max_length=50, 
        default="internal", 
        help_text="Search engine or service used."
    )
    referrer_url = models.URLField(
        null=True, 
        blank=True, 
        help_text="URL that referred the user to the search page."
    )
    search_context = models.CharField(
        max_length=255, 
        null=True, blank=True, 
        help_text="Context or origin of the search."
    )

    def __str__(self):
        return f"{self.user.username} - {self.search_term} on {self.date}"
        
        
class Article(BaseModel, SiteReaction):
    """
    Represents an Article which is typically more formal and structured, focusing on information, news, or educational content.
    """
    reaction_field = 'comment'
    comment_field = 'parent_comment'
    
    title = models.CharField(max_length=200, help_text="The headline of the article.")
    slug = models.SlugField(
        max_length=200, 
        unique=True,
        help_text="A URL-friendly version of the headline."
    )
    content_path = models.FileField(upload_to="articles/content/", help_text="The main content of the article.")
    author = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        related_name="articles",
        help_text="The author of the article."
    )
    published_date = models.DateTimeField(auto_now_add=True, help_text="When the article was published.")
    tags = models.ManyToManyField(
        'Tag', 
        related_name="articles", 
        blank=True,
        help_text="Keywords or tags for categorization."
    )
    featured_image = models.ImageField(
        upload_to="articles/images/", 
        null=True, 
        blank=True,
        help_text="A main image for the article."
    )
    excerpt = models.TextField(
        max_length=500,
        null=True, 
        blank=True,
        help_text="Short summary of the article."
    )
    views = models.IntegerField(default=0, help_text="Tracks how many times the article has been viewed.")

    def __str__(self):
        return self.title


class Blog(BaseModel, SiteReaction):
    """
    Represents a Blog which is often more personal and informal, focusing on storytelling, opinions, or lifestyle topics.
    """
    reaction_field = 'comment'
    comment_field = 'parent_comment'
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content_path = models.FileField(upload_to="blogs/content/")
    author = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        related_name="blogs"
    )
    published_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name="blogs", blank=True)
    likes = models.IntegerField(default=0, help_text="Tracks the number of likes the blog has received.")
    comments = models.ManyToManyField(
        'Comment', 
        related_name="blogs", 
        blank=True,
        help_text="Allows users to comment on the blog post."
    )
    cover_image = models.ImageField(
        upload_to="blogs/images/",
        null=True, 
        blank=True
    )
    is_published = models.BooleanField(default=False, help_text="Indicates whether the blog is a draft or published.")
    reading_time = models.IntegerField(help_text="Estimated reading time in minutes.")


    def __str__(self):
        return self.title
