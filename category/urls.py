# urls.py
from django.urls import path
from .views import MainCategoryListView

urlpatterns = [
    path('category-list', MainCategoryListView.as_view(), name='category-list'),
]
