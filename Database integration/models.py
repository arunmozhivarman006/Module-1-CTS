"""
Hands-On 7 - Migrations & Versioning — Alembic
File: models.py (updated from Hands-On 6 with new columns and table)

Changes from Hands-On 6 models.py:
  - Task 2 Step 1 : Added is_active (Boolean) column to Student
  - Task 2 Step 5 : Added new CourseSchedule table
"""

from sqlalchemy import (
    create_engine, Column, Integer, String,
    Date, Time, Decimal, ForeignKey, CHAR, Boolean
)
from sqlalchemy.orm import relationship, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:your_password@localhost/college_db_orm"
# For MySQL:
# DATABASE_URL = "mysql+mysqlconnector://root:your_password@localhost/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(100), nullable=False)
    head_of_dept  = Column(String(100))
    budget        = Column(Decimal(12, 2))

    students   = relationship("Student",   back_populates="department")
    courses    = relationship("Course",    back_populates="department")
    professors = relationship("Professor", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.department_id}, name='{self.dept_name}')>"


class Student(Base):
    __tablename__ = "students"

    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50), nullable=False)
    last_name       = Column(String(50), nullable=False)
    email           = Column(String(100), unique=True, nullable=False)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)
    is_active       = Column(Boolean, default=True)   # Added in Task 2 Step 1

    department  = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.student_id}, name='{self.first_name} {self.last_name}', active={self.is_active})>"


class Course(Base):
    __tablename__ = "courses"

    course_id     = Column(Integer, primary_key=True, autoincrement=True)
    course_name   = Column(String(150), nullable=False)
    course_code   = Column(String(20), unique=True)
    credits       = Column(Integer)
    max_seats     = Column(Integer, default=60)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    department  = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    schedules   = relationship("CourseSchedule", back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.course_id}, code='{self.course_code}')>"


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey("students.student_id"))
    course_id       = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade           = Column(CHAR(2))

    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course",  back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(student_id={self.student_id}, course_id={self.course_id}, grade='{self.grade}')>"


class Professor(Base):
    __tablename__ = "professors"

    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary        = Column(Decimal(10, 2))

    department = relationship("Department", back_populates="professors")

    def __repr__(self):
        return f"<Professor(id={self.professor_id}, name='{self.prof_name}')>"


class CourseSchedule(Base):
    """Added in Task 2 Step 5 — new table for course timetable"""
    __tablename__ = "course_schedules"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id   = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    day_of_week = Column(String(10), nullable=False)
    start_time  = Column(Time, nullable=False)
    end_time    = Column(Time, nullable=False)

    course = relationship("Course", back_populates="schedules")

    def __repr__(self):
        return f"<CourseSchedule(course_id={self.course_id}, day='{self.day_of_week}', {self.start_time}-{self.end_time})>"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("\nAll tables created in college_db_orm.")
