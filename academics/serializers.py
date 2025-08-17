from rest_framework import serializers
from .models import Department, AcademicYear, Course, Enrollment, CourseAssignment, Attendance
from accounts.serializers import StudentBasicSerializer, FacultyBasicSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""
    head_of_department = FacultyBasicSerializer(read_only=True)
    total_courses = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'description', 'head_of_department',
            'established_date', 'is_active', 'total_courses'
        ]
    
    def get_total_courses(self, obj):
        return obj.courses.filter(is_active=True).count()

class AcademicYearSerializer(serializers.ModelSerializer):
    """Serializer for Academic Year model"""
    
    class Meta:
        model = AcademicYear
        fields = ['id', 'year', 'start_date', 'end_date', 'is_current']

class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model"""
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    total_enrollments = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'code', 'credits', 'department', 'department_id',
            'semester', 'course_type', 'description', 'theory_hours', 
            'practical_hours', 'is_active', 'total_enrollments'
        ]
    
    def get_total_enrollments(self, obj):
        return obj.enrollments.filter(is_active=True).count()

class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model"""
    student = StudentBasicSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    academic_year = AcademicYearSerializer(read_only=True)
    academic_year_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_id', 'course', 'course_id',
            'academic_year', 'academic_year_id', 'enrollment_date',
            'grade', 'grade_points', 'is_active'
        ]

class CourseAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for Course Assignment model"""
    faculty = FacultyBasicSerializer(read_only=True)
    faculty_id = serializers.IntegerField(write_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    academic_year = AcademicYearSerializer(read_only=True)
    academic_year_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CourseAssignment
        fields = [
            'id', 'faculty', 'faculty_id', 'course', 'course_id',
            'academic_year', 'academic_year_id', 'is_course_coordinator',
            'assigned_date'
        ]

class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model"""
    student = StudentBasicSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    marked_by = FacultyBasicSerializer(read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'student_id', 'course', 'course_id',
            'date', 'is_present', 'remarks', 'marked_by', 'marked_at'
        ]