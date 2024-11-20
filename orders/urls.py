from django.urls import path
from . import views

app_name = 'orders'
urlpatterns=[
    path('', views.ApiOrderView.as_view(), name='api_order_list'),  # List all orders
    path('place_order',views.ApiPlaceOrder.as_view(),name='place_order'),
    path('payments',views.ApiPlaceOrder.as_view(),name='payments'),
    path('order/<str:order_number>/', views.ApiOrderDetail.as_view(), name='order_detail'),
   
   # path('products/search/', views.SearchAPIView.as_view(), name='product_search'),
]