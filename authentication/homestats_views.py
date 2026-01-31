from rest_framework import generics
from .models import HomeStats
from .homestats_serializers import HomeStatsSerializer

class HomeStatsListCreateView(generics.ListCreateAPIView):
    queryset = HomeStats.objects.filter(is_active=True).order_by('stat_type')
    serializer_class = HomeStatsSerializer

class HomeStatsUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeStats.objects.all()
    serializer_class = HomeStatsSerializer
    lookup_field = 'stat_type'