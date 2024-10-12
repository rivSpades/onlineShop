from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/products')
    stock=models.IntegerField()
    is_avaliable=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def get_absolute_url(self):#this method its necessary to redirect the page after create to somewhere , in this case to the detail of the record created
        return reverse("store:product_detail", args=[self.category.slug,self.slug])

    def __str__(self):
        return self.name


class VariationManager(models.Manager):

    def color(self):
        return super(VariationManager,self).filter(name='color', is_active=True)
    
    def size(self):
        return super(VariationManager,self).filter(name='size' , is_active=True)    


variation_choices = (
    ('color','color'),
    ('size','size'),
)
class Variation(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,choices=variation_choices)
    value=models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects=VariationManager()

    def __str__(self):
        return self.value