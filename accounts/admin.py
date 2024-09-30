from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Custom admin configuration for the Account model
class AccountAdmin(UserAdmin):
    # Fields to display in the list view of the admin
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links=('email','first_name','last_name')
    readonly_fields=('last_login','date_joined')
    ordering=('-date_joined',)
    # Keep these options empty
    filter_horizontal = ()  # Leave blank
    list_filter = ()        # Leave blank
    fieldsets = ()          # will make the password readonly

# Register the custom Account model with the admin
admin.site.register(Account, AccountAdmin)
