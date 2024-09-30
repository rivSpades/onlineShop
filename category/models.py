from django.db import models
from django.urls import reverse

class Category(models.Model):
    name= models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description=models.CharField(max_length=255,blank=True)
    image=models.ImageField(upload_to='photos/categories' , blank=True)

    class Meta:
        verbose_name ='category'
        verbose_name_plural="categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):#this method its necessary to redirect the page after create to somewhere , in this case to the detail of the record created
        return reverse("store:products_by_category", args=[self.slug])