from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.firebase_init import get_firebase_app
from app.schemas.user import UserOut
from app.services.auth_service import upsert_user

router = APIRouter(prefix="/auth", tags=["auth"])
bearer_scheme = HTTPBearer()


@router.post("/login", response_model=UserOut)
def login(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    get_firebase_app()
    try:
        decoded = firebase_auth.verify_id_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token")

    user = upsert_user(decoded, db)
    return user


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
