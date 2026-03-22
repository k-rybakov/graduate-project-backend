from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.progress import UserCourseAccess

MAGIC_SUCCESS_CARD = "4444333322221111"


def process_payment(user_id: str, course_id: int, card_number: str, db: Session) -> str:
    status = "success" if card_number == MAGIC_SUCCESS_CARD else "failed"

    payment = Payment(
        user_id=user_id,
        course_id=course_id,
        card_last_four=card_number[-4:] if len(card_number) >= 4 else card_number,
        status=status,
    )
    db.add(payment)

    if status == "success":
        existing = (
            db.query(UserCourseAccess)
            .filter(UserCourseAccess.user_id == user_id, UserCourseAccess.course_id == course_id)
            .first()
        )
        if not existing:
            access = UserCourseAccess(user_id=user_id, course_id=course_id)
            db.add(access)

    db.commit()
    return status
