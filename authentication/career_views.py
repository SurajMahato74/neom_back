from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import Career, JobApplication
from .career_serializers import CareerSerializer, JobApplicationSerializer, JobApplicationCreateSerializer

class CareerListView(generics.ListAPIView):
    """Public endpoint to list active careers"""
    serializer_class = CareerSerializer
    
    def get_queryset(self):
        queryset = Career.objects.filter(is_active=True)
        department = self.request.query_params.get('department')
        job_type = self.request.query_params.get('job_type')
        experience_level = self.request.query_params.get('experience_level')
        
        if department:
            queryset = queryset.filter(department__icontains=department)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
            
        return queryset

class CareerDetailView(generics.RetrieveAPIView):
    """Public endpoint to get career details"""
    queryset = Career.objects.filter(is_active=True)
    serializer_class = CareerSerializer

class JobApplicationCreateView(generics.CreateAPIView):
    """Public endpoint to submit job applications"""
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationCreateSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Application submitted successfully! We will review your application and contact you soon.',
                'application_id': serializer.instance.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin Views
class CareerManagementListCreateView(generics.ListCreateAPIView):
    """Admin endpoint to manage careers"""
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

class CareerManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin endpoint to manage individual careers"""
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

class JobApplicationManagementListView(generics.ListAPIView):
    """Admin endpoint to view all job applications"""
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    
    def get_queryset(self):
        queryset = JobApplication.objects.all()
        career_id = self.request.query_params.get('career')
        status_filter = self.request.query_params.get('status')
        
        if career_id:
            queryset = queryset.filter(career_id=career_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset

class JobApplicationManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin endpoint to manage individual job applications"""
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer