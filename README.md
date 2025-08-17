# College ERP System

A comprehensive College ERP system built in Django REST Framework for managing students, courses, faculty, and administrative functions, featuring role-based access (Admin, Faculty, Student).

---

## Features

- Role-based authentication & API security
- Student, Faculty, and Admin profiles
- Departments, Courses management
- Enrollment and attendance tracking
- RESTful API with permissions
- Admin panel for easy management

---

## Project Structure

college_erp/
├── venv/
├── college_erp_system/
│ ├── settings.py
│ ├── urls.py
│ └── ...
├── accounts/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── admin.py
│ └── urls.py
├── academics/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── admin.py
│ └── urls.py
├── core/
├── management/
│ └── commands/
│ └── load_sample_data.py
├── .vscode/
├── manage.py
├── requirements.txt






---

## Useful URLs

- Admin Panel: http://127.0.0.1:8000/admin/
- API Root: http://127.0.0.1:8000/api/

---

## API Endpoints

- `/api/accounts/users/`  - User management
- `/api/accounts/students/` - Student profiles
- `/api/accounts/faculty/` - Faculty profiles
- `/api/academics/departments/` - Departments
- `/api/academics/courses/` - Courses
- `/api/academics/enrollments/` - Enrollments
- `/api/academics/attendance/` - Attendance

---

## VS Code Settings

Setup files are available in `.vscode/settings.json` and `.vscode/launch.json` for Python linting and debugging.

---

## Notes

- Ensure **rest_framework.authtoken** is in your INSTALLED_APPS
- Use tokens for authenticated API requests

---

