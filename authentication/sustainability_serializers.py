from rest_framework import serializers
from .models import SustainabilityPillar

class SustainabilityPillarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SustainabilityPillar
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            request = self.context.get('request')
            if request:
                data['image'] = request.build_absolute_uri(instance.image.url)
            else:
                data['image'] = instance.image.url
        return data