from rest_framework import serializers
from .models import HomeStats

class HomeStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStats
        fields = '__all__'