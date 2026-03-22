from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.models.lesson import Lesson
from app.models.progress import UserProgress


def complete_lesson(user_id: str, lesson_id: int, db: Session) -> UserProgress:
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.deleted_at.is_(None)).first()
    if not lesson:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    stmt = (
        pg_insert(UserProgress)
        .values(user_id=user_id, lesson_id=lesson_id)
        .on_conflict_do_nothing(constraint="uq_user_lesson")
        .returning(UserProgress)
    )
    result = db.execute(stmt)
    db.commit()

    row = result.fetchone()
    if row:
        return row[0]
    return db.query(UserProgress).filter(
        UserProgress.user_id == user_id, UserProgress.lesson_id == lesson_id
    ).first()


def get_course_progress(user_id: str, course_id: int, db: Session) -> list[int]:
    rows = (
        db.query(UserProgress.lesson_id)
        .join(Lesson, Lesson.id == UserProgress.lesson_id)
        .filter(UserProgress.user_id == user_id, Lesson.course_id == course_id)
        .all()
    )
    return [r.lesson_id for r in rows]
