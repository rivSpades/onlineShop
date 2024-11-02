from django.urls import path
from . import views

app_name = 'store'
urlpatterns=[
    path('',views.StoreView.as_view(),name='store'),
    path('category/<slug:category_slug>/', views.StoreView.as_view(),name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(),name='product_detail'),
    path('search/', views.SearchAPIView.as_view(),name='search'),
    path('products/', views.ProductsAPIView.as_view(), name='products'),
    path('products/<slug:product_slug>/', views.ProductDetailAPIView.as_view(), name='product_details'),
   # path('products/search/', views.SearchAPIView.as_view(), name='product_search'),
]