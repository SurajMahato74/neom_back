from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AboutSection
from .about_serializers import AboutSectionSerializer

class AboutSectionView(APIView):
    def get(self, request):
        try:
            about = AboutSection.objects.filter(is_active=True).first()
            if not about:
                # Create default about section if none exists
                about = AboutSection.objects.create()
            serializer = AboutSectionSerializer(about)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            about = AboutSection.objects.filter(is_active=True).first()
            if not about:
                about = AboutSection.objects.create()
            
            serializer = AboutSectionSerializer(about, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)