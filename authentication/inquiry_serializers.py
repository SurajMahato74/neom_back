from rest_framework import serializers
from .models import Inquiry

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['id', 'full_name', 'email', 'phone_number', 'subject', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']