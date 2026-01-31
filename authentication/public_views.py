from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Distributor
from .distributor_serializers import DistributorSerializer

class PublicDistributorListView(generics.ListAPIView):
    queryset = Distributor.objects.filter(is_active=True)
    serializer_class = DistributorSerializer
    permission_classes = [AllowAny]