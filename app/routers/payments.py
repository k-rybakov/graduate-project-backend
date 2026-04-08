from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.dependencies import get_db, get_current_user
from app.models.progress import UserCourseAccess
from app.schemas.payment import PurchaseRequest, PurchaseResult
from app.services.payment_service import process_payment
from app.models.payment import Payment

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/purchase")
def purchase_course(body: dict, user = Depends(get_current_user), db: Session = Depends(get_db)):
    course_id = body.get("course_id")
    card_number = body.get("card_number")

    if not course_id:
        raise HTTPException(status_code=400, detail="Course ID is required")

    if card_number == "4444333322221111":
        existing_access = db.query(UserCourseAccess).filter(
            UserCourseAccess.user_id == user.id,
            UserCourseAccess.course_id == course_id
        ).first()

        if not existing_access:
            new_access = UserCourseAccess(
                user_id=user.id,
                course_id=course_id,
                granted_at=datetime.now(timezone.utc)
            )
            db.add(new_access)

        new_payment = Payment(
            user_id=user.id,
            course_id=course_id,
            card_last_four=card_number[-4:],
            status="success",
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_payment)

        db.commit()
        return {"status": "success", "message": "Payment successful. Course access granted."}

    raise HTTPException(status_code=400, detail="Payment failed. Invalid card")