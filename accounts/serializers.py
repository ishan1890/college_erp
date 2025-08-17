from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, FacultyProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'user_type', 'phone', 'date_of_birth', 'address', 
            'is_active', 'date_joined', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for Student Profile"""
    #user = UserSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(user_type='student'))
    user_details = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'user_details', 'student_id', 'enrollment_date',
            'current_semester', 'program', 'emergency_contact_name', 
            'emergency_contact_phone', 'is_active'
        ]
    
    def get_user_details(self, obj):
        return {
            'full_name': obj.user.get_full_name(),
            'email': obj.user.email,
            'user_type': obj.user.user_type
        }

class FacultyProfileSerializer(serializers.ModelSerializer):
    """Serializer for Faculty Profile"""
    #user = UserSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(user_type='faculty'))
    user_details = serializers.SerializerMethodField()
    
    class Meta:
        model = FacultyProfile
        fields = [
            'id', 'user', 'user_details', 'employee_id', 'department',
            'designation', 'joining_date', 'qualification',
            'experience_years', 'is_active'
        ]
    
    def get_user_details(self, obj):
        return {
            'full_name': obj.user.get_full_name(),
            'email': obj.user.email,
            'user_type': obj.user.user_type
        }

# Simple serializers for dropdowns
class UserBasicSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'user_type']

class StudentBasicSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'student_id', 'user', 'current_semester', 'program']

class FacultyBasicSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = FacultyProfile
        fields = ['id', 'employee_id', 'user', 'department', 'designation']