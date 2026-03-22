from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseListItem
from app.schemas.user import UserOut

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
def list_users(admin=Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at).all()


@router.get("/courses", response_model=list[CourseListItem])
def list_courses(admin=Depends(require_admin), db: Session = Depends(get_db)):
    courses = db.query(Course).filter(Course.deleted_at.is_(None)).order_by(Course.order_index).all()
    return [{**c.__dict__, "is_locked": False} for c in courses]


@router.post("/courses", response_model=CourseListItem, status_code=status.HTTP_201_CREATED)
def create_course(body: CourseCreate, admin=Depends(require_admin), db: Session = Depends(get_db)):
    course = Course(**body.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return {**course.__dict__, "is_locked": False}


@router.put("/courses/{course_id}", response_model=CourseListItem)
def update_course(course_id: int, body: CourseUpdate, admin=Depends(require_admin), db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id, Course.deleted_at.is_(None)).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(course, field, value)
    course.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(course)
    return {**course.__dict__, "is_locked": False}


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, admin=Depends(require_admin), db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id, Course.deleted_at.is_(None)).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    course.deleted_at = datetime.now(timezone.utc)
    db.commit()
