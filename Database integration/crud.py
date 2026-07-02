"""
Hands-On 6 - Task 2 & 3: SQLAlchemy ORM - CRUD Operations & Eager Loading
File: crud.py

QUERY COUNT COMPARISON (documented after running with echo=True):
  Without joinedload (Task 2 Step 5):
    - 1 query to fetch all enrollments
    - 1 query per enrollment to fetch student   -> N queries
    - 1 query per enrollment to fetch course    -> N queries
    - Total: 1 + N + N = 2N + 1 queries (for 10 enrollments = 21 queries)

  With joinedload (Task 3):
    - 1 single SQL query with LEFT OUTER JOINs
    - Total: 1 query regardless of data size
"""

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Department, Student, Course, Enrollment, Professor



DATABASE_URL = "postgresql+psycopg2://postgres:your_password@localhost/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()



print("\n" + "="*50)
print("INSERT: Departments")
print("="*50)

dept1 = Department(dept_name="Computer Science", head_of_dept="Dr. Ramesh Kumar", budget=850000.00)
dept2 = Department(dept_name="Electronics",      head_of_dept="Dr. Priya Nair",   budget=620000.00)
dept3 = Department(dept_name="Mechanical",       head_of_dept="Dr. Suresh Iyer",  budget=540000.00)

session.add_all([dept1, dept2, dept3])
session.commit()
print(f"Inserted: {dept1}, {dept2}, {dept3}")



print("\n" + "="*50)
print("INSERT: Students")
print("="*50)

s1 = Student(first_name="Arjun",   last_name="Mehta",  email="arjun.mehta@college.edu",
             date_of_birth=date(2003, 4, 12),  department_id=dept1.department_id, enrollment_year=2022)
s2 = Student(first_name="Priya",   last_name="Suresh", email="priya.suresh@college.edu",
             date_of_birth=date(2003, 7, 25),  department_id=dept1.department_id, enrollment_year=2022)
s3 = Student(first_name="Rohan",   last_name="Verma",  email="rohan.verma@college.edu",
             date_of_birth=date(2002, 11, 8),  department_id=dept2.department_id, enrollment_year=2021)
s4 = Student(first_name="Sneha",   last_name="Patel",  email="sneha.patel@college.edu",
             date_of_birth=date(2004, 1, 30),  department_id=dept3.department_id, enrollment_year=2023)
s5 = Student(first_name="Vikram",  last_name="Das",    email="vikram.das@college.edu",
             date_of_birth=date(2003, 9, 14),  department_id=dept1.department_id, enrollment_year=2022)

session.add_all([s1, s2, s3, s4, s5])
session.commit()
print(f"Inserted 5 students successfully.")


print("\n" + "="*50)
print("INSERT: Courses and Enrollments")
print("="*50)

c1 = Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4, department_id=dept1.department_id)
c2 = Course(course_name="Database Management Systems",  course_code="CS102", credits=3, department_id=dept1.department_id)
c3 = Course(course_name="Circuit Theory",               course_code="EC101", credits=3, department_id=dept2.department_id)

session.add_all([c1, c2, c3])
session.commit()

e1 = Enrollment(student_id=s1.student_id, course_id=c1.course_id, enrollment_date=date(2022, 7, 1), grade="A")
e2 = Enrollment(student_id=s1.student_id, course_id=c2.course_id, enrollment_date=date(2022, 7, 1), grade="B")
e3 = Enrollment(student_id=s2.student_id, course_id=c1.course_id, enrollment_date=date(2022, 7, 1), grade="B")
e4 = Enrollment(student_id=s3.student_id, course_id=c3.course_id, enrollment_date=date(2021, 7, 1), grade="A")

session.add_all([e1, e2, e3, e4])
session.commit()
print("Inserted 3 courses and 4 enrollments successfully.")


print("\n" + "="*50)
print("READ: Students in Computer Science")
print("="*50)

cs_students = (
    session.query(Student)
    .join(Department)
    .filter(Department.dept_name == "Computer Science")
    .all()
)
for student in cs_students:
    print(f"  {student.first_name} {student.last_name} | Year: {student.enrollment_year}")


print("\n" + "="*50)
print("READ: Enrollments with student + course (N+1 - no joinedload)")
print("="*50)

enrollments = session.query(Enrollment).all()
for enr in enrollments:
    # Each access of enr.student and enr.course fires a lazy-load SQL query
    print(f"  {enr.student.first_name} {enr.student.last_name} | {enr.course.course_name} | Grade: {enr.grade}")

print("\n[Check echo=True output above - count the number of SELECT statements fired]")


print("\n" + "="*50)
print("UPDATE: Student enrollment year")
print("="*50)

student_to_update = session.query(Student).filter_by(email="arjun.mehta@college.edu").first()
if student_to_update:
    student_to_update.enrollment_year = 2023
    session.commit()
    print(f"  Updated {student_to_update.first_name}'s enrollment year to {student_to_update.enrollment_year}")


print("\n" + "="*50)
print("DELETE: Remove an enrollment")
print("="*50)

enrollment_to_delete = session.query(Enrollment).filter_by(
    student_id=s2.student_id, course_id=c1.course_id
).first()

if enrollment_to_delete:
    session.delete(enrollment_to_delete)
    session.commit()
    print(f"  Deleted enrollment: Student {s2.first_name} from {c1.course_name}")

remaining = session.query(Enrollment).count()
print(f"  Remaining enrollments: {remaining}")


print("\n" + "="*50)
print("READ: Enrollments with joinedload (N+1 Fixed)")
print("="*50)

enrollments_eager = (
    session.query(Enrollment)
    .options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    )
    .all()
)

for enr in enrollments_eager:
    print(f"  {enr.student.first_name} {enr.student.last_name} | {enr.course.course_name} | Grade: {enr.grade}")

print("\n[Check echo=True output above - only 1 SELECT with JOINs should appear]")



print("\n" + "="*50)
print("SUMMARY")
print("="*50)
print("  Without joinedload : 2N+1 queries (lazy loading fires per row)")
print("  With joinedload    : 1 query (single SQL with LEFT OUTER JOIN)")
print("  For 10 enrollments : 21 queries reduced to 1")
print("="*50)

session.close()
