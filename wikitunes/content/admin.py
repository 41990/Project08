from django.contrib import admin
from .models import Post, Comment, Image, Video, Audio, Document, Tag, SiteReaction, SiteReport

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(Document)
admin.site.register(Tag)
admin.site.register(SiteReaction)
admin.site.register(SiteReport)


