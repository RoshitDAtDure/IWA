from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(lambda: None)):
    if not token:
        raise HTTPException(status_code=401)

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401)

    user = db.query(User).get(user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401)

    return user

def require_role(*roles):
    def guard(user = Depends(get_current_user)):
        if user.role.value not in roles:
            raise HTTPException(status_code=403)
        return user
    return guard

