from django.contrib import admin
from .models import WikiAdmin, Privilege

@admin.register(WikiAdmin)
class WikiAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_superadmin', 'can_validate_content')
    search_fields = ('user__username', 'user__email')

admin.site.register(WikiAdmin)
admin.site.register(Privilege)
