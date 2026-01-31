from rest_framework import generics, status
from rest_framework.response import Response
from .models import SustainabilityPillar
from .sustainability_serializers import SustainabilityPillarSerializer

class SustainabilityPillarListCreateView(generics.ListCreateAPIView):
    queryset = SustainabilityPillar.objects.filter(is_active=True).order_by('pillar_type')
    serializer_class = SustainabilityPillarSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class SustainabilityPillarUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SustainabilityPillar.objects.all()
    serializer_class = SustainabilityPillarSerializer
    lookup_field = 'pillar_type'
    
    def get_serializer_context(self):
        return {'request': self.request}