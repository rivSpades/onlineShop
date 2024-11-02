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
