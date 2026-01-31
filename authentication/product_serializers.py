from rest_framework import serializers
from .models import Product, ProductImage, ProductFeature

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'alt_text']
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'feature']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'