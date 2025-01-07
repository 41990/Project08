from django.contrib import admin

from .models import Account

class AccountAdmin(admin.UserAdmin):
    list_display = ('email', 'username', 'start_date', 'last_login')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account)

