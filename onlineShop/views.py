from django.shortcuts import render
from django.views.generic import View
from store.models import Product

class HomeView(View):
    def get(self,request):
        products = Product.objects.all().filter(is_avaliable=True)
        context={
            'products':products,
        }
        return render(request,'home.html',context)
