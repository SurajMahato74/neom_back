from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    featured_image_url = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['slug', 'views_count', 'published_at', 'created_at', 'updated_at']
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
        return None
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()

class BlogListSerializer(serializers.ModelSerializer):
    """Serializer for blog list view with limited fields"""
    featured_image_url = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'excerpt', 'featured_image_url', 'author', 
                 'is_featured', 'tags_list', 'read_time', 'views_count', 'published_at', 'created_at']
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
        return None
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()

class BlogDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog detail view with full content"""
    featured_image_url = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = '__all__'
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
        return None
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()