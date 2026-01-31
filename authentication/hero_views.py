from rest_framework import generics
from rest_framework.response import Response
from .models import HeroSection
from .hero_serializers import HeroSectionSerializer

class HeroSectionView(generics.RetrieveUpdateAPIView):
    serializer_class = HeroSectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_object(self):
        hero_section = HeroSection.objects.filter(is_active=True).first()
        if not hero_section:
            # Create default hero section if none exists
            hero_section = HeroSection.objects.create()
        return hero_section
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Handle image removal
        if request.data.get('remove_image') == 'true':
            if instance.image:
                instance.image.delete(save=False)
                instance.image = None
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)