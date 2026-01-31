from rest_framework import serializers
from .models import Career, JobApplication

class CareerSerializer(serializers.ModelSerializer):
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Career
        fields = '__all__'
    
    def get_applications_count(self, obj):
        return obj.applications.count()

class JobApplicationSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    cv_url = serializers.SerializerMethodField()
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applied_at', 'updated_at']
    
    def get_cv_url(self, obj):
        if obj.cv:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cv.url)
        return None

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['career', 'full_name', 'email', 'phone', 'cv', 'cover_letter']
    
    def validate_email(self, value):
        career = self.initial_data.get('career')
        if career and JobApplication.objects.filter(career_id=career, email=value).exists():
            raise serializers.ValidationError("You have already applied for this position.")
        return value