from django.contrib import admin
from .models import Department, AcademicYear, Course, Enrollment, CourseAssignment, Attendance

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin for Department model"""
    list_display = ['name', 'code', 'head_of_department', 'is_active']
    list_filter = ['is_active', 'established_date']
    search_fields = ['name', 'code']
    raw_id_fields = ['head_of_department']

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    """Admin for Academic Year model"""
    list_display = ['year', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    
    def save_model(self, request, obj, form, change):
        if obj.is_current:
            # Ensure only one academic year is current
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save_model(request, obj, form, change)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin for Course model"""
    list_display = [
        'code', 'name', 'department', 'semester', 'credits', 
        'course_type', 'is_active'
    ]
    list_filter = ['department', 'semester', 'course_type', 'is_active']
    search_fields = ['code', 'name']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin for Enrollment model"""
    list_display = [
        'get_student_name', 'get_student_id', 'course', 
        'academic_year', 'grade', 'is_active'
    ]
    list_filter = ['course__department', 'academic_year', 'grade', 'is_active']
    search_fields = [
        'student__student_id', 'student__user__first_name', 
        'student__user__last_name', 'course__code'
    ]
    raw_id_fields = ['student', 'course']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'
    
    def get_student_id(self, obj):
        return obj.student.student_id
    get_student_id.short_description = 'Student ID'

@admin.register(CourseAssignment)
class CourseAssignmentAdmin(admin.ModelAdmin):
    """Admin for Course Assignment model"""
    list_display = [
        'get_faculty_name', 'course', 'academic_year', 
        'is_course_coordinator'
    ]
    list_filter = ['academic_year', 'is_course_coordinator', 'course__department']
    search_fields = [
        'faculty__employee_id', 'faculty__user__first_name', 
        'faculty__user__last_name', 'course__code'
    ]
    raw_id_fields = ['faculty', 'course']
    
    def get_faculty_name(self, obj):
        return obj.faculty.user.get_full_name()
    get_faculty_name.short_description = 'Faculty Name'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin for Attendance model"""
    list_display = [
        'get_student_name', 'course', 'date', 'is_present'
    ]
    list_filter = ['date', 'is_present', 'course__department']
    search_fields = [
        'student__student_id', 'student__user__first_name', 
        'course__code'
    ]
    date_hierarchy = 'date'
    raw_id_fields = ['student', 'course', 'marked_by']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

