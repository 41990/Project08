from django.contrib import admin
from .models import Notification, NotificationLog

admin.site.register(Notification)
admin.site.register(NotificationLog)
