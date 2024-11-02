# cms/urls.py

from django.urls import path
from .views import BannerListView

urlpatterns = [
    path('banners-list/', BannerListView.as_view(), name='banner-list'),
]
