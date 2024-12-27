from django.db import models

from ..forums.models import Post, Comment
from django.utils.text import slugify
from ..tunes.models import BaseModel, dynamic_dir_path

def img_dir_path(instance, filename):
    
    folder = 'images'
    
    return dynamic_dir_path(instance, filename, folder)

def video_dir_path(instance, filename):
    
    folder = 'videos'
    
    return dynamic_dir_path(instance, filename, folder)
    
    
def audio_dir_path(instance, filename):
    
    folder = 'audios'
    
    return dynamic_dir_path(instance, filename, folder)
    
def text_dir_path(instance, filename):
    
    folder = 'messages'
    
    return dynamic_dir_path(instance, filename, folder)

class Media(BaseModel):
    """
    Represents the general multimedia concept associated to a post/comment.
    """
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    ]

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, help_text="Type of media.")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Upload timestamp.")
    tags = models.ManyToManyField('Tag', related_name='media')

    def __str__(self):
        return f"{self.media_type} - {self.file.name}"

        
        
class Image(Media):
    """
    Represents an image associated to a post/comment.
    """
    title = models.CharField(max_length=50, help_text="Title of the image.")
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        null=True,
        help_text="Associated post for the image."
    )
    comment = models.ForeignKey(
        Comment,
        on_delete = models.CASCADE,
        null=True,
        help_text="Associated comment for the image."
    )
    upload = models.ImageField(
        upload_to=img_dir_path,
        height_field="height",
        width_field="width",
        help_text="File containing uploaded image."
    )
    height = models.PositiveIntegerField(null=True, help_text="height of image in pixel/cm/mm.")
    width = models.PositiveIntegerField(null=True, help_text="width of image in pixel/cm/mm.")
    
    def __str__(self):
        return f"image for {self.post.title if self.post else self.comment.user.username}"


class Video(Media):
    """
    Represents a video associated to a post/comment.
    """
    title = models.CharField(max_length=50, help_text="Title of the video.")
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        null=True,
        help_text="Associated post for the video."
    )
    
    comment = models.ForeignKey(
        Comment,
        on_delete = models.CASCADE,
        null=True,
        help_text="Associated comment for the video."
    )
    upload = models.FileField(
        upload_to=video_dir_path,
        help_text="File containing uploaded video."
    )
    
    def __str__(self):
        return f"video for {self.post.title if self.post else self.comment.user.username}"
        
        
class Audio(Media):
    """
    Represents an audio associated to a post/comment.
    """
    title = models.CharField(max_length=50, help_text="Title of the audio.")
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        null=True,
        help_text="Associated post for the audio."
    )
    
    comment = models.ForeignKey(
        Comment,
        on_delete = models.CASCADE,
        null=True,
        help_text="Associated comment for the audio."
    )
    upload = models.FileField(
        upload_to=audio_dir_path,
        help_text="File containing uploaded audio."
    )
    
    def __str__(self):
        return f"audio for {self.post.title if self.post else self.comment.user.username}"
        
        
        
class Document(Media):
    """
    Represents a text/document associated to a post/comment.
    """
    title = models.CharField(max_length=50, help_text="Title of the text/document.")
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        null=True,
        help_text="Associated post for the text/document."
    )
    comment = models.ForeignKey(
        Comment,
        on_delete = models.CASCADE,
        null=True,
        help_text="Associated comment for the text/document."
    )
    upload = models.FileField(upload_to=text_dir_path, help_text="File containing uploaded text/document .")
    
    def __str__(self):
        return f"text/document for {self.post.title if self.post else self.comment.user.username}"
    
class Tag(models.Model):
    """
    Represents a versatile feature that enhances the functionality of your project by allowing 
    categorization, filtering, and organization of content. It’s especially useful in projects 
    involving blogs, articles, media, events, or any other entities where users might want to 
    group or search items based on specific keywords or topics.
    
    Categorization:

        Tags allow content to be grouped by keywords, making it easier for users to find related items.
    Search and Filtering:

        Tags can be used in search and filter functionalities to quickly narrow down content based on specific topics.
    SEO (Search Engine Optimization):

        Tags improve the discoverability of content by search engines.
    Content Recommendations:

        Use tags to suggest similar or related content to users.
    Analytics:

        Track the popularity of specific tags to understand user preferences and trends.
    """
    name = models.CharField(max_length=100, unique=True, help_text="The name of the tag.")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL-friendly version of the tag.")
    description = models.TextField(null=True, blank=True, help_text="Optional description of the tag.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the tag was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp of the last update to the tag.")
    popularity = models.IntegerField(default=0, help_text="How many times this tag has been used.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name