from django.db import models
from accounts.models import FacultyProfile, StudentProfile

class Department(models.Model):
    """Academic departments"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(
        FacultyProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='headed_departments'
    )
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

class AcademicYear(models.Model):
    """Academic years"""
    year = models.CharField(max_length=9, unique=True)  # e.g., "2024-2025"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return self.year
    
    class Meta:
        verbose_name = 'Academic Year'
        verbose_name_plural = 'Academic Years'

class Course(models.Model):
    """Courses offered by departments"""
    COURSE_TYPE_CHOICES = [
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('lab', 'Laboratory'),
        ('project', 'Project'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    credits = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    semester = models.PositiveIntegerField()
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, default='core')
    description = models.TextField(blank=True)
    theory_hours = models.PositiveIntegerField(default=0)
    practical_hours = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

class Enrollment(models.Model):
    """Student course enrollments"""
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'),
        ('C+', 'C+'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
        ('I', 'Incomplete'), ('W', 'Withdrawn'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    grade_points = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
    
    class Meta:
        unique_together = ['student', 'course', 'academic_year']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

class CourseAssignment(models.Model):
    """Faculty course assignments"""
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    is_course_coordinator = models.BooleanField(default=False)
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.faculty} teaches {self.course} ({self.academic_year})"
    
    class Meta:
        unique_together = ['faculty', 'course', 'academic_year']
        verbose_name = 'Course Assignment'
        verbose_name_plural = 'Course Assignments'

class Attendance(models.Model):
    """Student attendance records"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    remarks = models.CharField(max_length=200, blank=True)
    marked_by = models.ForeignKey(FacultyProfile, on_delete=models.SET_NULL, null=True, blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student} - {self.course} ({self.date}): {status}"
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'