from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from .models import Product
from category.models import Category
# Create your views here.

class StoreView(View):
    def get(self,request,category_slug=None):

        if category_slug:
            category=get_object_or_404(Category,slug=category_slug)
            products=Product.objects.filter(category=category,is_avaliable=True)
        else:
            products = Product.objects.all().filter(is_avaliable=True)

        products_count=products.count()
        context={
            'products':products,
            'products_count':products_count,
        }

        return render(request,'store/store.html',context)

class ProductDetailView(View):
    def get(self,request,category_slug,product_slug=None):


        return render(request,'store/product_detail.html')

