# orm_shell_examples.py — run these lines inside: python manage.py shell
from django.db.models import Count, F
from courses.models import Department, Course, Student, Enrollment

# --- Step 16: create sample data ---
cs = Department.objects.create(name="Computer Science", head_of_dept="Dr. Rao", budget=500000)
ee = Department.objects.create(name="Electrical Engineering", head_of_dept="Dr. Iyer", budget=350000)

Course.objects.create(name="Data Structures", code="CS101", credits=4, department=cs)
Course.objects.create(name="Operating Systems", code="CS201", credits=4, department=cs)
Course.objects.create(name="Circuits I", code="EE101", credits=3, department=ee)
Course.objects.create(name="Signals & Systems", code="EE201", credits=3, department=ee)

Student.objects.create(first_name="Asha", last_name="Verma", email="asha@college.edu", department=cs, enrollment_year=2024)
Student.objects.create(first_name="Rohan", last_name="Nair", email="rohan@college.edu", department=cs, enrollment_year=2024)
Student.objects.create(first_name="Meera", last_name="Shah", email="meera@college.edu", department=ee, enrollment_year=2023)
Student.objects.create(first_name="Karan", last_name="Patel", email="karan@college.edu", department=ee, enrollment_year=2023)
Student.objects.create(first_name="Divya", last_name="Rao", email="divya@college.edu", department=cs, enrollment_year=2025)

# --- Step 17: filter across a ForeignKey ---
cs_courses = Course.objects.filter(department__name="Computer Science")

# --- Step 18: annotate course count per department ---
dept_counts = Department.objects.annotate(course_count=Count("courses")).values("name", "course_count")

# --- Step 19: select_related to avoid N+1 queries ---
students_with_dept = Student.objects.select_related("department").all()
from django.db import connection
print(len(connection.queries))  # should show a single JOIN query, not one-per-student

# --- Step 20: bulk update using F() — computed in the DB, not in Python ---
Department.objects.update(budget=F("budget") * 1.1)
