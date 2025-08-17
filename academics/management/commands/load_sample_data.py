from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, FacultyProfile
from academics.models import Department, AcademicYear, Course, Enrollment, CourseAssignment
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Load sample data for testing'
    
    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create Academic Year
        current_year, created = AcademicYear.objects.get_or_create(
            year='2024-2025',
            defaults={
                'start_date': date(2024, 7, 1),
                'end_date': date(2025, 6, 30),
                'is_current': True
            }
        )
        
        # Create Departments
        cs_dept, created = Department.objects.get_or_create(
            code='CS',
            defaults={
                'name': 'Computer Science',
                'description': 'Department of Computer Science and Engineering'
            }
        )
        
        math_dept, created = Department.objects.get_or_create(
            code='MATH',
            defaults={
                'name': 'Mathematics',
                'description': 'Department of Mathematics'
            }
        )
        
        # Create Faculty User
        faculty_user, created = User.objects.get_or_create(
            username='prof_smith',
            defaults={
                'email': 'smith@college.edu',
                'first_name': 'John',
                'last_name': 'Smith',
                'user_type': 'faculty'
            }
        )
        if created:
            faculty_user.set_password('password123')
            faculty_user.save()
        
        # Create Faculty Profile
        faculty_profile, created = FacultyProfile.objects.get_or_create(
            employee_id='FAC001',
            defaults={
                'user': faculty_user,
                'department': cs_dept,   # ✅ ForeignKey object
                'designation': 'Professor',
                'joining_date': date(2020, 1, 1)
            }
        )
        
        # Create Student User
        student_user, created = User.objects.get_or_create(
            username='student_doe',
            defaults={
                'email': 'doe@student.college.edu',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'user_type': 'student'
            }
        )
        if created:
            student_user.set_password('password123')
            student_user.save()
        
        # Create Student Profile
        student_profile, created = StudentProfile.objects.get_or_create(
            student_id='STU2024001',
            defaults={
                'user': student_user,
                'enrollment_date': date(2024, 7, 1),
                'current_semester': 1,
                'program': 'Computer Science'  # adjust if it's ForeignKey
            }
        )
        
        # Create Courses
        course1, created = Course.objects.get_or_create(
            code='CS101',
            defaults={
                'name': 'Introduction to Programming',
                'credits': 3,
                'department': cs_dept,
                'semester': 1,
                'description': 'Basic programming concepts'
            }
        )
        
        course2, created = Course.objects.get_or_create(
            code='MATH101',
            defaults={
                'name': 'Calculus I',
                'credits': 4,
                'department': math_dept,
                'semester': 1,
                'description': 'Differential calculus'
            }
        )
        
        # Create Course Assignment
        assignment, created = CourseAssignment.objects.get_or_create(
            faculty=faculty_profile,
            course=course1,
            academic_year=current_year,
            defaults={
                'is_course_coordinator': True
            }
        )
        
        # Create Enrollments
        enrollment1, created = Enrollment.objects.get_or_create(
            student=student_profile,
            course=course1,
            academic_year=current_year
        )
        
        enrollment2, created = Enrollment.objects.get_or_create(
            student=student_profile,
            course=course2,
            academic_year=current_year
        )
        
        self.stdout.write(
            self.style.SUCCESS('✅ Successfully loaded sample data')
        )
