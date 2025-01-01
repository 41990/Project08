from django.contrib import admin
from content.models import Comment, count_items, average_items

def count_comments(modeladmin, request, queryset):
    count_items(queryset, 'comment', 'comments')

# Register your models here.
