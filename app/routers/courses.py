from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.dependencies import get_db, get_current_user
from app.schemas.course import CourseListItem, CourseDetail
from app.schemas.lesson import LessonOut
from app.models.lesson import Lesson, LessonSection
from app.models.course import Course
from app.services.course_service import get_courses_for_user, get_course_detail, get_lesson

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseListItem])
def list_courses(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_courses_for_user(user, db)


@router.get("/{slug}", response_model=CourseDetail)
def course_detail(slug: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_course_detail(slug, user, db)


@router.get("/{slug}/lessons", response_model=list[LessonOut])
def get_course_lessons_public(slug: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.slug == slug, Course.deleted_at.is_(None)).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")


    lessons = (
        db.query(Lesson)
        .options(
            joinedload(Lesson.sections)
            .joinedload(LessonSection.tasks)
        )
        .filter(Lesson.course_id == course.id, Lesson.deleted_at.is_(None))
        .order_by(Lesson.order_index)
        .all()
    )
    return lessons


@router.get("/{slug}/lessons/{lesson_slug}", response_model=LessonOut)
def lesson_detail(slug: str, lesson_slug: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_lesson(slug, lesson_slug, user, db)