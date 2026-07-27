from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, init_models, Course
from schemas import CourseCreate, CourseUpdate, CourseResponse

# Step 82: URL versioning (/api/v1/...) is what's used below - simple, visible
# in the URL, easy to test in a browser. The alternative is header-based
# versioning (Accept: application/vnd.api+json;version=1) - it keeps URLs
# clean/stable, but requires setting a header on every request/tool, so
# it's harder to explore or test from a plain browser.


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(title="Course Management API", version="1.0.0", lifespan=lifespan)


# --- Step 85: standardised error envelope for every HTTPException ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    code_map = {404: "NOT_FOUND", 400: "BAD_REQUEST", 401: "UNAUTHORIZED", 409: "CONFLICT"}
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {
            "code": code_map.get(exc.status_code, "ERROR"),
            "message": exc.detail,
            "field": None,
        }},
    )


@app.get("/api/v1/courses/", tags=["Courses"])
async def list_courses(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Step 83/84: offset pagination envelope + case-insensitive search."""
    stmt = select(Course)
    if search:
        like = f"%{search}%"
        stmt = stmt.where(or_(Course.name.ilike(like), Course.code.ilike(like)))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(stmt.offset(offset).limit(page_size))
    courses = result.scalars().all()

    base = "/api/v1/courses/"
    has_next = offset + page_size < total
    has_prev = page > 1
    return {
        "count": total,
        "next": f"{base}?page={page + 1}&page_size={page_size}" if has_next else None,
        "previous": f"{base}?page={page - 1}&page_size={page_size}" if has_prev else None,
        "results": [CourseResponse.model_validate(c).model_dump() for c in courses],
    }


@app.post("/api/v1/courses/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=["Courses"])
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    # Step 81: Location header pointing at the new resource
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CourseResponse.model_validate(new_course).model_dump(),
        headers={"Location": f"/api/v1/courses/{new_course.id}/"},
    )


@app.get("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    return course


@app.put("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def replace_course(course_id: int, payload: CourseCreate, db: AsyncSession = Depends(get_db)):
    """PUT = full replace, all fields required (CourseCreate has no optional fields)."""
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    for field, value in payload.model_dump().items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.patch("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def partial_update_course(course_id: int, payload: CourseUpdate, db: AsyncSession = Depends(get_db)):
    """PATCH = partial update, only supplied fields change."""
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete("/api/v1/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    await db.delete(course)
    await db.commit()
    return None
