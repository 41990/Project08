from datetime import datetime
import uuid
from django.db import models
from django.db.models import Avg

from tunes.models import BaseModel
from accounts.models import Account
from content.models import CATEGORY_CHOICES, ReactionMixin

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


def forum_data_desc_dir_path(instance, filename):
    
    return dynamic_dir_path(instance, filename, 'forums')



class BaseModel(models.Model):
    is_valid = models.BooleanField(default=True, help_text="Indicates if the object is valid.")
    
    class Meta:
        abstract = True



class Forum(BaseModel, ReactionMixin):
    """
    Represents a forum associated with an account, containing categories and ratings.
    """
    reaction_field = 'forum'
    comment_field = 'forum'
    
    title = models.CharField(max_length=50, help_text="Title of the forum.")
    description = models.FileField(upload_to=forum_data_desc_dir_path, help_text="File describing the forum content.")
    category = models.CharField(
        max_length=10, 
        choices=CATEGORY_CHOICES,
        default='CAT_0',
        help_text="Forum category."
    )
    pub_date = models.DateTimeField(auto_now=True, help_text="Date when the forum was published.")
    current_date = models.DateField(auto_now=True, help_text="Last updated date.")
    account = models.ForeignKey(
        Account,
        on_delete = models.CASCADE,
        help_text="Associated account for the forum."
    )
    
    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return f"Forum Title: {self.title}"
    
    
