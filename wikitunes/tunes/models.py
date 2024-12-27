from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from ..accounts.models import Account, CustomUser

from ..forums.models import Post, average_items, count_items, Comment

def privilege_dir_path(instance, filename):
    return f"privileges/docs/{datetime.now().strftime('%Y/%m/%d')}/{filename}"

def reactions_dir_path(instance, filename):
    return f"site/reactions/{datetime.now().strftime('%Y/%m/%d')}/{filename}"

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

class BaseModel(models.Model):
    is_valid = models.BooleanField(default=True, help_text="Indicates if the object is valid.")
    
    class Meta:
        abstract = True

class WikiAdmin(models.Model):
    """
    Represents the present application administrator who also possesses an account.
    """
    admin_names = models.CharField(max_length=50, help_text="Admin names.")
    password = models.CharField(max_length=254, help_text="Hashed administrator password.")
    current_date = models.DateField(auto_now=True, help_text="Last updated date.")
    account = models.OneToOneField(
        Account,
        on_delete = models.CASCADE,
        help_text="Associated admin account."
    )
    
    def __str__(self):
        return "admin: %s" %self.admin_names
        
    def save(self, *args, **kwargs):
        """
        Overridden save method to hash the password before saving.
        """
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
    def check_password(self, raw_password):
        """
        Verify the provided password against the stored hashed password.
        """
        return check_password(raw_password, self.password)
    
    
class Privilege(BaseModel):
    """
    Represents the privileges given to either the admin or account owner or custom user within the application.
    """
    owner = models.CharField(max_length=50, help_text="Who the privilege applies to.")
    title = models.CharField(max_length=50, help_text="Title of the privilege.")
    description = models.FileField(upload_to=privilege_dir_path, help_text="Description of the privilege.")
    current_date = models.DateField(auto_now=True, help_text="Last updated date.")
    admin = models.ForeignKey(
        WikiAdmin,
        on_delete = models.CASCADE,
        null = True, 
        blank=True,
        limit_choices_to={'is_staff': True},  # Restrict to staff users
        help_text="Admin to which privilege applies if applicable."
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        null = True, 
        blank=True,
        help_text="Custom user to which privilege applies if applicable."
    )
    account = models.ForeignKey(
        Account,
        on_delete = models.CASCADE,
        null = True,
        blank=True,
        help_text="Account to which privilege applies if applicable."
    )
    
    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return f"privilege for {self.owner}"
    
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