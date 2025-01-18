# cms/serializers.py

from rest_framework import serializers
from .models import Banner,Logo

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class LogoSerializer(serializers.ModelSerializer):
    logo_img_url = serializers.SerializerMethodField()  # Generate the full URL for the logo image

    class Meta:
        model = Logo
        fields = ['id', 'name', 'logo_img', 'is_active', 'created_at', 'updated_at', 'logo_img_url']

    def get_logo_img_url(self, obj):
        """Generate the full URL for the logo image."""
        request = self.context.get('request')  # Get the current request context
        if obj.logo_img and request:
            return request.build_absolute_uri(obj.logo_img.url)
        return None