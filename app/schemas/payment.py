from pydantic import BaseModel


class PurchaseRequest(BaseModel):
    course_id: int
    card_number: str


class PurchaseResult(BaseModel):
    status: str
    message: str
