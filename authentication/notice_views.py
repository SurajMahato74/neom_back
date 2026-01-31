from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count, Q
from .models import Notice
from .notice_serializers import NoticeSerializer

class NoticeListCreateView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class NoticeUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_update(self, serializer):
        # Only update fields that are provided
        instance = self.get_object()
        if 'image' not in self.request.FILES:
            serializer.validated_data.pop('image', None)
        if 'attachment' not in self.request.FILES:
            serializer.validated_data.pop('attachment', None)
        serializer.save()

class PublicNoticeListView(generics.ListAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Notice.objects.filter(is_active=True)

class PublicFeaturedNoticeView(generics.ListAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Notice.objects.filter(is_active=True, is_featured=True)[:1]

class NoticeArchiveStatsView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Get count of notices by year
        archive_stats = Notice.objects.filter(is_active=True).extra(
            select={'year': 'strftime("%%Y", published_date)'}
        ).values('year').annotate(count=Count('id')).order_by('-year')
        
        return Response(archive_stats)