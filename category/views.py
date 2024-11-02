# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MainCategory
from .serializers import MainCategorySerializer,CategorySerializer

class MainCategoryListView(APIView):
    def get(self, request):
        main_categories = MainCategory.objects.prefetch_related('category_set')
        serializer = MainCategorySerializer(main_categories, many=True)
        
        # Add related categories to the response
        response_data = []
        for main_category in main_categories:
            data = serializer.data
            categories = CategorySerializer(main_category.category_set.all(), many=True).data
            response_data.append({
                "id": main_category.id,
                "name": main_category.name,
                "slug": main_category.slug,
                "description": main_category.description,
                "image": main_category.image.url if main_category.image else None,
                "categories": categories  # Add categories here
            })
        
        return Response(response_data)
