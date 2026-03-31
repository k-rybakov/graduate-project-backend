from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseListItem
from app.schemas.user import UserOut

from app.schemas.lesson import LessonCreate, LessonUpdate, LessonOut
from app.models.lesson import Lesson
from app.services.admin_service import save_lesson_content

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
def list_users(admin=Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at).all()


@router.get("/courses", response_model=list[CourseListItem])
def list_courses(admin=Depends(require_admin), db: Session = Depends(get_db)):
    courses = db.query(Course).filter(Course.deleted_at.is_(None)).order_by(Course.order_index).all()
    return [{**c.__dict__, "is_locked": False} for c in courses]


@router.get("/courses/{course_id}/lessons", response_model=list[LessonOut])
def list_course_lessons(course_id: int, admin=Depends(require_admin), db: Session = Depends(get_db)):
    lessons = (
        db.query(Lesson)
        .filter(Lesson.course_id == course_id, Lesson.deleted_at.is_(None))
        .order_by(Lesson.order_index)
        .all()
    )
    return lessons


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


@router.post("/lessons", response_model=LessonOut)
def create_lesson(body: LessonCreate, admin=Depends(require_admin), db: Session = Depends(get_db)):
    existing = db.query(Lesson).filter(Lesson.course_id == body.course_id, Lesson.slug == body.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists for this course")

    lesson = Lesson(
        course_id=body.course_id,
        title=body.title,
        slug=body.slug,
        order_index=body.order_index,
        is_free=body.is_free
    )
    db.add(lesson)
    db.flush()

    if body.sections:
        save_lesson_content(db, lesson, body.sections)

    db.commit()
    return lesson


@router.delete("/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(lesson_id: int, admin=Depends(require_admin), db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()


@router.put("/lessons/{lesson_id}", response_model=LessonOut)
def update_lesson(
    lesson_id: int,
    body: LessonCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson.title = body.title
    lesson.slug = body.slug
    lesson.order_index = body.order_index
    lesson.is_free = body.is_free

    save_lesson_content(db, lesson, body.sections)

    db.commit()
    db.refresh(lesson)
    return lesson