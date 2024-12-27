from django.db import models
from django.db.models import Avg

from ..accounts.models import Account, CustomUser, acc_data_desc_dir_path, user_comment_dir_path

from ..tunes.models import BaseModel, ReactionMixin, dynamic_dir_path

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


def forum_data_desc_dir_path(instance, filename):
    
    return dynamic_dir_path(instance, filename, 'forums')

CATEGORY_CHOICES = [
    ('CAT_0','Choose'),
    ('CAT_1','Category 1'),
    ('CAT_2','Category 2'),
    ('CAT_3','Category 3'),
    ('CAT_4','Category 4'),
    ('CAT_5','Category 5'),
    ('CAT_6','Category 6')
]

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