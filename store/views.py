from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import View
from django.db.models import Q
from .models import Product
from category.models import Category,MainCategory
from cart.models import CartItem,Cart
from .serializers import ProductSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
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





class ProductsAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Base queryset to only include available products
        queryset = Product.objects.filter(is_avaliable=True)

        # Filter by category slug if provided
        category_slug = self.request.query_params.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        # Filter by main category slug if provided
        main_category_slug = self.request.query_params.get('main_category')
        if main_category_slug:
            main_category = get_object_or_404(MainCategory, slug=main_category_slug)
            queryset = queryset.filter(category__main_category=main_category)

        # Filter by keyword if provided
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(category__name__icontains=keyword)
            )

        return queryset

    
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.filter(is_avaliable=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'product_slug'    

class SearchAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):

        
        # Search by keyword in name or description
        keyword = self.request.query_params.get('keyword')
        print(keyword)
        if keyword:
            queryset = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(category__name__icontains=keyword),is_avaliable=True)

        return queryset    