from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import UserCourseAccess
from app.models.user import User


def _has_course_access(user: User, course: Course, db: Session) -> bool:
    if user.role == "admin":
        return True
    if course.is_free:
        return True
    access = (
        db.query(UserCourseAccess)
        .filter(UserCourseAccess.user_id == user.id, UserCourseAccess.course_id == course.id)
        .first()
    )
    return access is not None


def get_courses_for_user(user: User, db: Session) -> list[dict]:
    courses = (
        db.query(Course)
        .filter(Course.deleted_at.is_(None))
        .order_by(Course.order_index)
        .all()
    )
    result = []
    for course in courses:
        locked = not _has_course_access(user, course, db)
        result.append({**course.__dict__, "is_locked": locked})
    return result


def get_course_detail(slug: str, user: User, db: Session) -> dict:
    course = db.query(Course).filter(Course.slug == slug, Course.deleted_at.is_(None)).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    lessons = (
        db.query(Lesson)
        .filter(Lesson.course_id == course.id, Lesson.deleted_at.is_(None))
        .order_by(Lesson.order_index)
        .all()
    )
    locked = not _has_course_access(user, course, db)
    return {**course.__dict__, "is_locked": locked, "lessons": lessons}


def get_lesson(course_slug: str, lesson_slug: str, user: User, db: Session):
    course = db.query(Course).filter(Course.slug == course_slug, Course.deleted_at.is_(None)).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if not _has_course_access(user, course, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Course access required")

    lesson = (
        db.query(Lesson)
        .filter(Lesson.course_id == course.id, Lesson.slug == lesson_slug, Lesson.deleted_at.is_(None))
        .first()
    )
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    return lesson
