from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas.progress import ProgressOut, CourseProgressOut
from app.services.progress_service import complete_lesson, get_course_progress

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/lessons/{lesson_id}/complete", response_model=ProgressOut)
def mark_lesson_complete(lesson_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return complete_lesson(user.id, lesson_id, db)


@router.get("/courses/{course_id}", response_model=CourseProgressOut)
def course_progress(course_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    completed_ids = get_course_progress(user.id, course_id, db)
    return CourseProgressOut(course_id=course_id, completed_lesson_ids=completed_ids)
