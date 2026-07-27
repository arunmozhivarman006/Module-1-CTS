# models.py — copy this into handson_01_django_setup/coursemanager/courses/models.py
# then run: python manage.py makemigrations && python manage.py migrate

from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_dept = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    credits = models.PositiveSmallIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="students")
    enrollment_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        unique_together = [["student", "course"]]

    def __str__(self):
        return f"{self.student} -> {self.course}"
