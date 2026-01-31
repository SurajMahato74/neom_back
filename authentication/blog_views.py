from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q, F
from .models import Blog
from .blog_serializers import BlogSerializer, BlogListSerializer, BlogDetailSerializer

# Public Views
class BlogListView(generics.ListAPIView):
    """Public endpoint to list published blogs"""
    serializer_class = BlogListSerializer
    
    def get_queryset(self):
        queryset = Blog.objects.filter(status='published')
        
        # Filter by tags
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(content__icontains=search) |
                Q(tags__icontains=search)
            )
        
        return queryset

class BlogDetailView(generics.RetrieveAPIView):
    """Public endpoint to get blog details"""
    queryset = Blog.objects.filter(status='published')
    serializer_class = BlogDetailSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        Blog.objects.filter(pk=instance.pk).update(views_count=F('views_count') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class FeaturedBlogListView(generics.ListAPIView):
    """Public endpoint to get featured blogs"""
    queryset = Blog.objects.filter(status='published', is_featured=True)
    serializer_class = BlogListSerializer

# Admin Views
class BlogManagementListCreateView(generics.ListCreateAPIView):
    """Admin endpoint to manage blogs"""
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        queryset = Blog.objects.all()
        status_filter = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(tags__icontains=search)
            )
        
        return queryset

class BlogManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin endpoint to manage individual blogs"""
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    parser_classes = [MultiPartParser, FormParser]