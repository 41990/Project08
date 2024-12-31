from datetime import datetime
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.conf import settings
from django.utils.text import slugify

from accounts.models import Account, CustomUser, img_dir_path, text_dir_path


def dynamic_dir_path(instance, filename, folder):
    """
    Generate dynamic file path based on the instance attributes.
    
    Parameters:
        instance: Model instance where the file is being uploaded.
        filename: Original file name.
        folder: The subdirectory for the file (e.g., 'images', 'videos').

    Returns:
        str: Dynamically constructed file path.
    """
    ext = filename.split('.')[-1]
    
    # Generate a new file name with a timestamp to avoid overwrites
    new_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    
    if hasattr(instance, 'account') and instance.account:
        return f"account_{instance.account.id}/{folder}/{datetime.now().strftime('%Y/%m/%d')}/{new_filename}"
    
    if hasattr(instance, 'user') and instance.user:
        return f"user_{instance.user.id}/{folder}/{datetime.now().strftime('%Y/%m/%d')}/{new_filename}"
    
    return f"uploads/others/{folder}/{datetime.now().strftime('%Y/%m/%d')}/{new_filename}"


def count_items(filter_key, filter_value, class_variable):
    """
    Counts filtered items of a given instance.
    
    Parameters:
        filter_key (str): The field name to filter on.
        filter_value: The value to filter the field by.
        class_variable: Model class which defines the item instances being counted

    Returns:
        int: The number of filtered items.
    """
    try:
        filtered_items = class_variable.objects.filter(**{filter_key: filter_value})
        return filtered_items.count()
    except Exception as e:
        # Log the error or return a default value
        return 0
    
def average_items(filter_key, filter_value, class_variable, field_name):
    """
    Calculates the average of a given distribution of filtered items.
    
    Parameters:
        filter_key (str): The field name to filter on.
        filter_value: The value to filter the field by.
        class_variable: Model class which defines the item instances being counted.
        field_name (str): The name of the field to calculate the average for.

    Returns:
        float: The average value of the filtered field.
    """
    try:
        filtered_items = class_variable.objects.filter(**{filter_key: filter_value})
        return filtered_items.aggregate(Avg(field_name))[f"{field_name}__avg"] or 0
    except Exception as e:
        # Log the error or return a default value
        return 0

def reactions_dir_path(instance, filename):
    return f"site/reactions/{datetime.now().strftime('%Y/%m/%d')}/{filename}"

def validate_file_size(file):
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(f"The file size exceeds the maximum limit of {settings.MAX_UPLOAD_SIZE / (1024 * 1024)} MB.")


def video_dir_path(instance, filename):
    
    folder = 'videos'
    
    return dynamic_dir_path(instance, filename, folder)
    
    
def audio_dir_path(instance, filename):
    
    folder = 'audios'
    
    return dynamic_dir_path(instance, filename, folder)

def acc_data_desc_dir_path(instance, filename):
    
    return dynamic_dir_path(instance, filename, 'posts')

def user_comment_dir_path(instance, filename):
    
    return dynamic_dir_path(instance, filename, 'comments')   

CATEGORY_CHOICES = [
    ('CAT_0','Choose'),
    ('CAT_1','Category 1'),
    ('CAT_2','Category 2'),
    ('CAT_3','Category 3'),
    ('CAT_4','Category 4'),
    ('CAT_5','Category 5'),
    ('CAT_6','Category 6')
]

class BaseModel(models.Model):
    is_valid = models.BooleanField(default=True, help_text="Indicates if the object is valid.")
    
    class Meta:
        abstract = True
        
        
class ReactionMixin:
    def num_reactions(self):
        try:
            return count_items(self.reaction_field, self, SiteReaction)
        except Exception as e:
            # Log the error or return a default value
            return 0

    def ave_ratings(self):
        try:
            return average_items(self.reaction_field, self, SiteReaction, 'num_star')
        except Exception as e:
            # Log the error or return a default value
            return 0

    def num_comments(self):
        try:
            return count_items(self.comment_field, self, Comment)
        except Exception as e:
            # Log the error or return a default value
            return 0



class Post(BaseModel, ReactionMixin):
    """
    Represents a post associated with an account, containing categories and ratings.
    """
    reaction_field = 'post'
    comment_field = 'post'
    
    title = models.CharField(max_length=50, help_text="Title of the post.")
    description = models.FileField(upload_to=acc_data_desc_dir_path, help_text="File describing the post content.")
    category = models.CharField(
        max_length=10, 
        choices=CATEGORY_CHOICES,
        default='CAT_0',
        help_text="Post category."
    )
    pub_date = models.DateTimeField(auto_now=True, help_text="Date when the post was published.")
    current_date = models.DateField(auto_now=True, help_text="Last updated date.")
    account = models.ForeignKey(
        Account,
        on_delete = models.CASCADE,
        help_text="Associated account for the post."
    )
    tags = models.ManyToManyField('Tag', related_name='posts')
    
    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return f"Post Title: {self.title}"


class Comment(BaseModel, ReactionMixin):
    """
    Represents a comment on a post, including its rating and validation status.
    """
    reaction_field = 'comment'
    comment_field = 'parent_comment'
    
    message = models.FileField(upload_to=user_comment_dir_path, help_text="Content of the comment.")
    pub_date = models.DateTimeField(auto_now=True, help_text="Date when the comment was published.")
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        help_text="User who made the comment."
    )
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        null=True, 
        blank=True,
        help_text="Associated post for the comment."
    )
    parent_comment = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='replies', 
        help_text="The parent comment, if this comment is a reply."
    )
    tags = models.ManyToManyField('Tag', related_name='comments')
    
    def __str__(self):
        return f"Comment on {self.post.title if self.post else self.parent_comment.user.username} by {self.user.username}"
        
    def save(self, *args, **kwargs):
        if self.parent_comment == self:
            raise ValueError("A comment cannot reply to itself.")
        super().save(*args, **kwargs)


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
        validators=[validate_file_size],
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
        validators=[validate_file_size],
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
        validators=[validate_file_size],
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
    
    
class SiteReaction(models.Model):
    """
    Represents a reaction to a post/comment, by a custom user.
    """
    message = models.FileField(upload_to=reactions_dir_path, help_text="File containing message associated to reaction")
    user  = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        help_text="User who makes the reaction"
    )
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        help_text="Associated post for the reaction."
    )
    comment = models.OneToOneField(
        Comment,
        on_delete = models.CASCADE,
        help_text="Associated comment for the reaction."
    )
    ONE_STAR = 1
    TWO_STAR = 2
    THREE_STAR = 3
    FOUR_STAR = 4
    FIVE_STAR = 5
    STAR_CATEGORY={
        ONE_STAR:'Very bad post/comment',
        TWO_STAR:'Bad post/comment',
        THREE_STAR:'Good post/comment',
        FOUR_STAR:'Impressive post/comment',
        FIVE_STAR:'Outstanding post/comment'
    }
    num_star = models.IntegerField(
        choices=STAR_CATEGORY,
        default=1,
        help_text="Number of stars for reaction."
    )
    
    def __str__(self):
        return f"Reaction to {self.post.title if self.post else self.comment.user.username} by {self.user.username}"
    
    
class SiteReport(models.Model):
    """
    Represents a report on a post/comment, by a custom user.
    """
    message = models.FileField(upload_to=reactions_dir_path, help_text="File containing message associated to user report")
    user  = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        help_text="User who makes the report"
    )
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        help_text="Associated post for the report."
    )
    comment = models.OneToOneField(
        Comment,
        on_delete = models.CASCADE,
        help_text="Associated comment for the report."
    )
    SPAM = 'Spam'
    ABUSE = 'Abuse'
    INAPPROPRIATE = 'Inappropriate'
    OTHER = 'Other'
    REPORT_CATEGORY={
        SPAM:'Spam',
        ABUSE:'Abuse',
        INAPPROPRIATE:'Inappropriate',
        OTHER:'Other'
    }
    category = models.CharField(
        max_length=20,
        choices=REPORT_CATEGORY,
        default='Spam',
        help_text="Category of the report."
    )
    
    def __str__(self):
        return f"Report on {self.post.title if self.post else self.comment.user.username} by {self.user.username}"
    
class SiteBookmark(models.Model):
    """
    Represents a bookmark on a post/comment, by a custom user.
    """
    user  = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        help_text="User who makes the bookmark"
    )
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        help_text="Associated post for the bookmark."
    )
    comment = models.OneToOneField(
        Comment,
        on_delete = models.CASCADE,
        help_text="Associated comment for the bookmark."
    )
    
    def __str__(self):
        return f"Bookmark on {self.post.title if self.post else self.comment.user.username} by {self.user.username}"
    
    
class SiteEmoji(models.Model):
    """
    Represents an emoji reaction to a post/comment, by a custom user.
    """
    user  = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        help_text="User who makes the emoji reaction"
    )
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        help_text="Associated post for the emoji reaction."
    )
    comment = models.OneToOneField(
        Comment,
        on_delete = models.CASCADE,
        help_text="Associated comment for the emoji reaction."
    )
    LIKE = 'Like'
    LOVE = 'Love'
    HAHA = 'Haha'
    WOW = 'Wow'
    SAD = 'Sad'
    ANGRY = 'Angry'
    EMOJI_CATEGORY={
        LIKE:'Like',
        LOVE:'Love',
        HAHA:'Haha',
        WOW:'Wow',
        SAD:'Sad',
        ANGRY:'Angry'
    }
    emoji = models.CharField(
        max_length=20,
        choices=EMOJI_CATEGORY,
        default='Like',
        help_text="Emoji reaction to the post/comment."
    )
    
    def __str__(self):
        return f"Emoji reaction to {self.post.title if self.post else self.comment.user.username} by {self.user.username}"