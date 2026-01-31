from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = [
            'id',
            'title',
            'short_description',
            'description',
            'notice_type',
            'image',
            'attachment',
            'tags',
            'tags_list',
            'is_featured',
            'is_active',
            'published_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_tags_list(self, obj):
        return obj.get_tags_list()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request:
            if instance.image:
                data['image'] = (
                    request.scheme
                    + "://"
                    + request.get_host()
                    + "/api"
                    + instance.image.url
                )

            if instance.attachment:
                data['attachment'] = (
                    request.scheme
                    + "://"
                    + request.get_host()
                    + "/api"
                    + instance.attachment.url
                )

        return data
