from rest_framework import serializers
from .models import TikTokVideo

class TikTokVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TikTokVideo
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.thumbnail:
            request = self.context.get('request')
            if request:
                data['thumbnail'] = request.build_absolute_uri(instance.thumbnail.url)
            else:
                data['thumbnail'] = instance.thumbnail.url
        return data