from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, init_models, Course, Student, Enrollment
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


# --- Step 75: OpenAPI metadata customisation ---
app = FastAPI(
    title="Course Management API",
    description="Backend API for managing departments, courses, students and enrollments.",
    version="1.0.0",
    contact={"name": "Digital Nurture 5.0", "email": "poc@college.edu"},
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "API running"}


# ============================= Courses =============================
@app.get("/api/courses/", response_model=List[CourseResponse], tags=["Courses"])
async def list_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Course)
    if department_id is not None:
        stmt = stmt.where(Course.department_id == department_id)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return result.scalars().all()


@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="The created course",
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.put("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(course_id: int, payload: CourseUpdate, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete("/api/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    await db.delete(course)
    await db.commit()
    return None


@app.get("/api/courses/{course_id}/students/", response_model=List[StudentResponse], tags=["Courses"])
async def course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    if not await db.get(Course, course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    stmt = (
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.course_id == course_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


# ============================= Students =============================
@app.get("/api/students/", response_model=List[StudentResponse], tags=["Students"])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.post("/api/students/", response_model=StudentResponse, status_code=201, tags=["Students"])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@app.get("/api/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.delete("/api/students/{student_id}", status_code=204, tags=["Students"])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await db.delete(student)
    await db.commit()
    return None


# ============================= Enrollments =============================
def send_confirmation_email(student_email: str):
    # Simulated notification - runs AFTER the response has already been sent.
    print(f"Sending confirmation to {student_email}")


@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, enrollment.student_id)
    course = await db.get(Course, enrollment.course_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_enrollment = Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    # Step 73/74: response returns immediately; email "sends" after.
    background_tasks.add_task(send_confirmation_email, student.email)
    return new_enrollment


@app.get("/api/enrollments/", response_model=List[EnrollmentResponse], tags=["Enrollments"])
async def list_enrollments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Enrollment))
    return result.scalars().all()


@app.delete("/api/enrollments/{enrollment_id}", status_code=204, tags=["Enrollments"])
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    enrollment = await db.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    await db.delete(enrollment)
    await db.commit()
    return None
