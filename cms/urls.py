# cms/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('banners-list/', BannerListView.as_view(), name='banner-list'),
    path('logo/', LogoView.as_view(), name='logo'),
]
