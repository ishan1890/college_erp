from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import StudentProfile, FacultyProfile
from .serializers import (
    UserSerializer, StudentProfileSerializer, FacultyProfileSerializer,
    StudentBasicSerializer, FacultyBasicSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class StudentProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Student Profile"""
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user type"""
        user = self.request.user
        if user.user_type == 'student':
            return StudentProfile.objects.filter(user=user)
        elif user.user_type == 'admin':
            return StudentProfile.objects.all()
        else:  # faculty
            return StudentProfile.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current student's profile"""
        if request.user.user_type != 'student':
            return Response(
                {'error': 'Only students can access this endpoint'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            profile = StudentProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class FacultyProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Faculty Profile"""
    queryset = FacultyProfile.objects.all()
    serializer_class = FacultyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user type"""
        user = self.request.user
        if user.user_type == 'faculty':
            return FacultyProfile.objects.filter(user=user)
        elif user.user_type == 'admin':
            return FacultyProfile.objects.all()
        else:  # student
            return FacultyProfile.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current faculty's profile"""
        if request.user.user_type != 'faculty':
            return Response(
                {'error': 'Only faculty can access this endpoint'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            profile = FacultyProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except FacultyProfile.DoesNotExist:
            return Response(
                {'error': 'Faculty profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )