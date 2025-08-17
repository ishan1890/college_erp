from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, FacultyProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_active']
    list_filter = ['user_type', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone', 'date_of_birth', 'address')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone', 'date_of_birth', 'address')
        }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin for Student Profile"""
    list_display = [
        'student_id', 'get_full_name', 'program', 'current_semester', 
        'enrollment_date', 'is_active'
    ]
    list_filter = ['current_semester', 'program', 'is_active', 'enrollment_date']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    raw_id_fields = ['user']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    """Admin for Faculty Profile"""
    list_display = [
        'employee_id', 'get_full_name', 'department', 'designation', 
        'joining_date', 'is_active'
    ]
    list_filter = ['department', 'designation', 'is_active', 'joining_date']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__email']
    raw_id_fields = ['user']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'