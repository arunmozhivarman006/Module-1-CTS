# models.py — copy into flask_coursemanager/courses/models.py
from extensions import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100))
    budget = db.Column(db.Numeric(12, 2), default=0)
    courses = db.relationship("Course", back_populates="department")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "head_of_dept": self.head_of_dept, "budget": float(self.budget)}


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    department = db.relationship("Department", back_populates="courses")

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "code": self.code,
            "credits": self.credits, "department_id": self.department_id,
        }


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    enrollment_year = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id, "first_name": self.first_name, "last_name": self.last_name,
            "email": self.email, "department_id": self.department_id,
            "enrollment_year": self.enrollment_year,
        }


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    enrollment_date = db.Column(db.Date, server_default=db.func.current_date())
    grade = db.Column(db.String(2), nullable=True)
    student = db.relationship("Student")
    course = db.relationship("Course")

    def to_dict(self):
        return {
            "id": self.id, "student_id": self.student_id, "course_id": self.course_id,
            "enrollment_date": str(self.enrollment_date), "grade": self.grade,
        }
