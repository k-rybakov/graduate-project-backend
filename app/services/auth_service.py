from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.user import User


def upsert_user(decoded_token: dict, db: Session) -> User:
    uid = decoded_token["uid"]
    email = decoded_token.get("email", "")
    display_name = decoded_token.get("name")

    user = db.query(User).filter(User.id == uid).first()
    if user:
        user.email = email
        user.display_name = display_name
        user.updated_at = datetime.now(timezone.utc)
    else:
        user = User(id=uid, email=email, display_name=display_name, role="user")
        db.add(user)

    db.commit()
    db.refresh(user)
    return user
