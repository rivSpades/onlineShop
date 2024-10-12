from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import Q
from .models import Product
from category.models import Category
from cart.models import CartItem,Cart
# Create your views here.

class StoreView(View):
    def get(self,request,category_slug=None):

        if category_slug:
            category=get_object_or_404(Category,slug=category_slug)
            products=Product.objects.filter(category=category,is_avaliable=True)
        else:
            products = Product.objects.all().filter(is_avaliable=True).order_by('id')
            
        paginator = Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)

        products_count=products.count()
        context={
            'products':paged_products,
            'products_count':products_count,
        }

        return render(request,'store/store.html',context)

class ProductDetailView(View):
    def get(self,request,category_slug,product_slug):
        product = get_object_or_404(Product,category__slug=category_slug,slug=product_slug, is_avaliable=True) #category__slug access the slug field in the category object
        in_cart = CartItem.objects.filter(cart__cart_session_id=Cart._get_cart_id(request),product=product).exists()
        context={
            'product':product,
            'in_cart':in_cart,
        }
        return render(request,'store/product_detail.html',context)
    
class SearchView(View):
    def get(self,request):
      
        if 'keyword' in request.GET:
            keyword=request.GET.get('keyword')
            if keyword:
                products=Product.objects.filter(Q(description__icontains=keyword) | Q( name__icontains=keyword),is_avaliable=True)
            else:
                products = Product.objects.all().filter(is_avaliable=True).order_by('id')

        
        products_count=products.count()
        context={
            'products':products,
            'products_count':products_count,
        }
        return render(request,'store/store.html',context)    

