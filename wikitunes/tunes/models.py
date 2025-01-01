from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from accounts.models import Account, Visitor

def privilege_dir_path(instance, filename):
    return f"privileges/docs/{datetime.now().strftime('%Y/%m/%d')}/{filename}"

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

class WikiAdmin(AbstractBaseUser):
    """
    Represents the present application administrator who also possesses an account.
    """
    password = models.CharField(max_length=254, help_text="Hashed administrator password.")
    can_validate_content = models.BooleanField(default=True)
    account = models.OneToOneField(
        Account,
        on_delete = models.CASCADE,
        help_text="Associated admin account."
    )
    
    def __str__(self):
        return f"admin: {self.account.user.username}"
        
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
    permission = models.ManyToManyField('auth.Permission', help_text="Permissions associated with the privilege.")
    description = models.FileField(upload_to=privilege_dir_path, help_text="Description of the privilege.")
    pub_date = models.DateField(auto_now=True, help_text="Last updated date.")
    admin = models.ForeignKey(
        WikiAdmin,
        on_delete = models.CASCADE,
        null = True, 
        blank=True,
        limit_choices_to={'is_staff': True},  # Restrict to staff users
        help_text="Admin to which privilege applies if applicable."
    )
    user = models.ForeignKey(
        Visitor,
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
    