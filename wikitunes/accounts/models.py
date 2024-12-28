from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.conf import settings


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

def img_dir_path(instance, filename):
    
    folder = 'images'
    
    return dynamic_dir_path(instance, filename, folder)

def text_dir_path(instance, filename):
    
    folder = 'messages'
    
    return dynamic_dir_path(instance, filename, folder)

def validate_file_size(file):
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(f"The file size exceeds the maximum limit of {settings.MAX_UPLOAD_SIZE / (1024 * 1024)} MB.")

def roles_dir_path(instance, filename):
    return f"roles/docs/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class CustomUser(AbstractUser):
    """
    Represents a custom user with additional fields for address and country.
    Extends Django's AbstractUser for flexibility in user management.
    """
    email = models.EmailField(unique=True, help_text="Unique email address of the user.")
    address = models.CharField(max_length=50, help_text="User's address.")
    country = models.CharField(max_length=50, help_text="Country where the user resides.")
    
    def __str__(self):
        return self.username

class Account(models.Model):
    """
    Represents a user account with additional metadata like location, email, and registration IP.
    """
    account_names = models.CharField(max_length=50, help_text="Name of the account holder.")
    password = models.CharField(max_length=254, help_text="Hashed password for the account.")
    account_location = models.CharField(max_length=50, help_text="Physical location associated with the account.")
    profile_picture = models.ImageField(
        upload_to=img_dir_path,
        validators=[validate_file_size],
        height_field="height",
        width_field="width",
        help_text="File containing uploaded profile image."
    )
    height = models.PositiveIntegerField(null=True, help_text="height of image in pixel/cm/mm.")
    width = models.PositiveIntegerField(null=True, help_text="width of image in pixel/cm/mm.")
    bio = models.FileField(upload_to=text_dir_path, help_text="File containing uploaded bio.")
    reg_device_ip = models.GenericIPAddressField(
        protocol = 'both',
        unpack_ipv4 = False,
        help_text="Registration device IP address."
    )
    start_date = models.DateTimeField(auto_now=True, help_text="The date and time when the account was created.")
    current_date = models.DateField(auto_now=True, help_text="Last updated date.")
    user = models.OneToOneField(
        CustomUser,
        on_delete = models.CASCADE,
        help_text="Associated custom user."
    )
    
    def __str__(self):
        return f"Account: {self.account_names}"
    
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


class Role(models.Model):
    """
    Represents a role associated with an account, containing categories.
    """
    ROLE_ZERO = 'Select role'
    ROLE_ONE = 'Educator'
    ROLE_TWO = 'Researcher'
    ROLE_THREE = 'Owner/CEO/Proprietor'
    ROLE_FOUR = 'Project Team member'
    ROLE_FIVE = 'Learner/student'
    ROLE_SIX = 'Other'
    ROLE_CHOICES = {
        ROLE_ZERO:'Choose',
        ROLE_ONE:'Role 1',
        ROLE_TWO:'Role 2',
        ROLE_THREE:'Role 3',
        ROLE_FOUR:'Role 4',
        ROLE_FIVE:'Role 5',
        ROLE_SIX:'Role 6',
    }
    role_name = models.CharField(
        max_length=30, 
        choices=ROLE_CHOICES,
        default=ROLE_ZERO,
        help_text="Role category."
    )
    
    account = models.ForeignKey(
        Account,
        on_delete = models.CASCADE,
        help_text="Associated account for the role."
    )
    
    def __str__(self):
        return f"Role name: {self.role_name}"
