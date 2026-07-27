from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from database import get_db, init_models, User, Course
from schemas import UserCreate, UserResponse, Token, CourseCreate, CourseResponse
from security import get_password_hash, verify_password, create_access_token, decode_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(title="Course Management API", version="1.0.0", lifespan=lifespan)

# Step 94: allow the frontend dev server to call this API. CORS is enforced
# by the BROWSER (based on these response headers), not by this server -
# it does not protect server-to-server calls.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


# ============================= Auth =============================
@app.post("/api/v1/auth/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = (await db.execute(select(User).where(User.email == user.email))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = User(email=user.email, hashed_password=get_password_hash(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.post("/api/v1/auth/login/", response_model=Token, tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == form_data.username))).scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(subject=user.email)
    return Token(access_token=token)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        email = decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


# ============================= Courses (GET open, write protected) =============================
@app.get("/api/v1/courses/", response_model=list[CourseResponse], tags=["Courses"])
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    return result.scalars().all()


@app.post("/api/v1/courses/", response_model=CourseResponse, status_code=201, tags=["Courses"])
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.delete("/api/v1/courses/{course_id}", status_code=204, tags=["Courses"])
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    await db.delete(course)
    await db.commit()
    return None


# OAuth2 Authorization Code flow (concept, step 95):
# Instead of the client collecting a password directly (what we did above),
# the user is redirected to the auth provider's own login page. After they
# approve, the provider redirects back with a short-lived "authorization
# code". The client's backend then exchanges that code (plus a client
# secret) for an access token via a server-to-server call. This means the
# client app never sees the user's password, and is the standard flow for
# "Sign in with Google/GitHub/etc" style third-party logins. Our simple JWT
# login is appropriate for a first-party app where the API owns the user
# accounts directly.
