from rest_framework import generics
from .models import Distributor
from .distributor_serializers import DistributorSerializer

class DistributorListCreateView(generics.ListCreateAPIView):
    queryset = Distributor.objects.filter(is_active=True).order_by('name')
    serializer_class = DistributorSerializer

class DistributorUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Distributor.objects.all()
    serializer_class = DistributorSerializer