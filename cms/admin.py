from django.contrib import admin
from .models import Banner, Logo

class BannerAdmin(admin.ModelAdmin):
    # Customizing the layout with fieldsets
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'banner_img', 'discount', 'black_friday')
        }),
        ('Instructions', {
            'fields': (),  # No field here, just displaying instructions
            'description': 'Suggested dimensions for the banner: 1415x700 pixels.'
        }),
    )

    list_display = ('id', 'title', 'discount', 'black_friday')  # Removed created_date and modified_date
    search_fields = ('title',)
    list_filter = ('black_friday',)

class LogoAdmin(admin.ModelAdmin):
    # Customizing the layout with fieldsets
    fieldsets = (
        (None, {
            'fields': ('name', 'logo_img', 'is_active')
        }),
        ('Instructions', {
            'fields': (),  # No field here, just displaying instructions
            'description': 'Suggested dimensions for the logo: 113x37 pixels.'
        }),
    )

    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')  # Added created_at and updated_at for Logo
    search_fields = ('name',)
    list_filter = ('is_active',)

# Register the Banner model with custom admin class
admin.site.register(Banner, BannerAdmin)

# Register the Logo model with custom admin class
admin.site.register(Logo, LogoAdmin)
