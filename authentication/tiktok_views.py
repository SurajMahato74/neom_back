from rest_framework import generics
from .models import TikTokVideo
from .tiktok_serializers import TikTokVideoSerializer

class TikTokVideoListCreateView(generics.ListCreateAPIView):
    queryset = TikTokVideo.objects.filter(is_active=True).order_by('order', 'created_at')
    serializer_class = TikTokVideoSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class TikTokVideoUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TikTokVideo.objects.all()
    serializer_class = TikTokVideoSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}