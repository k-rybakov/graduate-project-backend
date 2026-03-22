from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas.payment import PurchaseRequest, PurchaseResult
from app.services.payment_service import process_payment

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/purchase", response_model=PurchaseResult)
def purchase(body: PurchaseRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    status = process_payment(user.id, body.course_id, body.card_number, db)
    if status == "success":
        return PurchaseResult(status="success", message="Payment successful. Course access granted.")
    return PurchaseResult(status="failed", message="Payment failed. Invalid card number.")
