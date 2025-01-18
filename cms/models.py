# cms/models.py

from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    banner_img = models.ImageField(upload_to='images/banners/')  # This saves the image to /static/images/banners/
    discount = models.CharField(max_length=3)  # Using CharField since discounts may include percentages
    black_friday = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Logo(models.Model):
    name = models.CharField(max_length=255)  # A name or description for the logo
    logo_img = models.ImageField(upload_to='images/logos/')  # Saves the logo image to /static/images/logos/
    is_active = models.BooleanField(default=True)  # Flag to determine if the logo is currently active
    created_at = models.DateTimeField(auto_now_add=True)  # To track when the logo was created
    updated_at = models.DateTimeField(auto_now=True)  # To track when the logo was last updated

    def __str__(self):
        return self.name