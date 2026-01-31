import logging
from rest_framework import generics
from rest_framework.response import Response
from .models import HeroSection
from .hero_serializers import HeroSectionSerializer

logger = logging.getLogger(__name__)

class HeroSectionView(generics.RetrieveUpdateAPIView):
    serializer_class = HeroSectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_object(self):
        logger.info("Fetching hero section data")
        hero_section = HeroSection.objects.filter(is_active=True).first()
        if not hero_section:
            logger.warning("No active hero section found, creating default")
            # Create default hero section if none exists
            hero_section = HeroSection.objects.create()
        logger.info(f"Hero section retrieved: {hero_section.id}")
        return hero_section
    
    def retrieve(self, request, *args, **kwargs):
        try:
            logger.info(f"Hero section GET request from {request.META.get('REMOTE_ADDR')}")
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving hero section: {str(e)}")
            raise
    
    def update(self, request, *args, **kwargs):
        logger.info(f"Hero section UPDATE request from {request.META.get('REMOTE_ADDR')}")
        instance = self.get_object()
        
        # Handle image removal
        if request.data.get('remove_image') == 'true':
            logger.info("Removing hero section image")
            if instance.image:
                instance.image.delete(save=False)
                instance.image = None
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        logger.info(f"Hero section updated successfully: {instance.id}")
        return Response(serializer.data)