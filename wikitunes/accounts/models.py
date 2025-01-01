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


class Visitor(models.Model):
    """
    Represents a visitor with additional fields for address and country.
    Extends Django's AbstractUser for flexibility in user management.
    """
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='visitor_set',  # Custom related name
        blank=True,
    )
    username = models.CharField(max_length=150, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # For tracking
    session_id = models.CharField(max_length=255, blank=True, null=True)  # Unique session
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username or f"Anonymous Visitor ({self.ip_address})"
    

class Account(AbstractUser):
    """
    Represents a user account with additional metadata like location, email, and registration IP.
    """
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
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=True, help_text="The date and time when the account was created.")
    current_date = models.DateField(auto_now=True, help_text="Last updated date.")
    
    def __str__(self):
        return f"Account: {self.username}"
    
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
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class SocialRole(models.Model):
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
