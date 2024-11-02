from django.urls import path
from . import views


app_name='cart'

urlpatterns=[
path('',views.ApiCartView.as_view() , name='cart'),
path('add_cart/<int:product_id>/',views.ApiAddCartView.as_view(),name="add_cart"),
path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.RemoveCartView.as_view(),name="remove_cart"),

]