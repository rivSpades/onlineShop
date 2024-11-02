# models.py
from django.db import models
from django.urls import reverse

class MainCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'main category'
        verbose_name_plural = "main categories"

    def __str__(self):
        return self.name

class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, blank=True, null=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:products_by_category", args=[self.slug])
