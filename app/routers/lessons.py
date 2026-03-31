from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.schemas.lesson import LessonOut

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/{course_slug}/{lesson_slug}", response_model=LessonOut)
def get_full_lesson(course_slug: str, lesson_slug: str, db: Session = Depends(get_db)):
    lesson = (
        db.query(Lesson)
        .join(Course)
        .filter(
            Course.slug == course_slug,
            Lesson.slug == lesson_slug,
            Lesson.deleted_at.is_(None)
        )
        .first()
    )

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return lesson