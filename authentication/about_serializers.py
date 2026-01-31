from rest_framework import serializers
from .models import AboutSection

class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = ['id', 'title', 'description', 'is_active', 'updated_at']
        read_only_fields = ['id', 'updated_at']