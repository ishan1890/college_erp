from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Department, AcademicYear, Course, Enrollment, CourseAssignment, Attendance
from .serializers import (
    DepartmentSerializer, AcademicYearSerializer, CourseSerializer,
    EnrollmentSerializer, CourseAssignmentSerializer, AttendanceSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department model"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Admin only for CUD operations"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class AcademicYearViewSet(viewsets.ModelViewSet):
    """ViewSet for Academic Year model"""
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Admin only for CUD operations"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current academic year"""
        try:
            current_year = AcademicYear.objects.get(is_current=True)
            serializer = self.get_serializer(current_year)
            return Response(serializer.data)
        except AcademicYear.DoesNotExist:
            return Response(
                {'error': 'No current academic year set'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course model"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Admin for CUD operations"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter courses based on query parameters"""
        queryset = Course.objects.filter(is_active=True)
        
        # Filter by department
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        
        # Filter by semester
        semester = self.request.query_params.get('semester')
        if semester:
            queryset = queryset.filter(semester=semester)
        
        return queryset

class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment model"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter enrollments based on user type"""
        user = self.request.user
        queryset = Enrollment.objects.filter(is_active=True)
        
        if user.user_type == 'student':
            # Students see only their enrollments
            queryset = queryset.filter(student__user=user)
        elif user.user_type == 'faculty':
            # Faculty see enrollments for their assigned courses
            assigned_courses = CourseAssignment.objects.filter(
                faculty__user=user
            ).values_list('course', flat=True)
            queryset = queryset.filter(course__in=assigned_courses)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_enrollments(self, request):
        """Get current student's enrollments"""
        if request.user.user_type != 'student':
            return Response(
                {'error': 'Only students can access this endpoint'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        enrollments = Enrollment.objects.filter(
            student__user=request.user, 
            is_active=True
        )
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)

class CourseAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Course Assignment model"""
    queryset = CourseAssignment.objects.all()
    serializer_class = CourseAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Admin only for CUD operations"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter assignments based on user type"""
        user = self.request.user
        queryset = CourseAssignment.objects.all()
        
        if user.user_type == 'faculty':
            # Faculty see only their assignments
            queryset = queryset.filter(faculty__user=user)
        
        return queryset

class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Attendance model"""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter attendance based on user type"""
        user = self.request.user
        queryset = Attendance.objects.all()
        
        if user.user_type == 'student':
            # Students see only their attendance
            queryset = queryset.filter(student__user=user)
        elif user.user_type == 'faculty':
            # Faculty see attendance for their assigned courses
            assigned_courses = CourseAssignment.objects.filter(
                faculty__user=user
            ).values_list('course', flat=True)
            queryset = queryset.filter(course__in=assigned_courses)
        
        return queryset.order_by('-date')
    
    @action(detail=False, methods=['get'])
    def my_attendance(self, request):
        """Get current student's attendance"""
        if request.user.user_type != 'student':
            return Response(
                {'error': 'Only students can access this endpoint'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        attendance = Attendance.objects.filter(student__user=request.user)
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)