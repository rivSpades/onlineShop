# cms/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Banner,Logo
from .serializers import BannerSerializer,LogoSerializer

class BannerListView(APIView):
    
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)


class LogoView(APIView):
    def get(self, request):
        logos = Logo.objects.filter(is_active=True)  # You can filter logos by is_active, if desired
        serializer = LogoSerializer(logos, many=True)
        return Response(serializer.data)