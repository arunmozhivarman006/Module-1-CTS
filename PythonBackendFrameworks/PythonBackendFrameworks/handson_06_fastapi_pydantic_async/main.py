from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from database import get_db, init_models, Course
from schemas import CourseCreate, CourseResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(title="Course Management API", version="1.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "API running"}


# --- Task 1, Step 60: POST validated against CourseCreate ---
@app.post("/api/courses/", response_model=CourseResponse, status_code=201)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


# --- Task 2, Step 62: path parameter, auto-validated as int ---
@app.get("/api/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# --- Task 2, Step 63/67: pagination + filtering via query params ---
@app.get("/api/courses/", response_model=List[CourseResponse])
async def list_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Course)
    if department_id is not None:
        stmt = stmt.where(Course.department_id == department_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
