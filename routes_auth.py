from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.core.security import create_token, hash_password, verify_password
from backend.db.models import User
from backend.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


class Credentials(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(c: Credentials, db: Session = Depends(get_db)):
    u = db.scalar(select(User).where(User.username == c.username))
    if not u or not verify_password(c.password, u.password_hash):
        raise HTTPException(401, "bad credentials")
    return {"access_token": create_token(u.id, u.role, dept=u.department_code), "role": u.role}


@router.post("/register", status_code=201)
def register(c: Credentials, db: Session = Depends(get_db)):
    """تسجيل مواطن فقط. الأدوار الأخرى بتتعمل من الـ admin / seed."""
    if db.scalar(select(User).where(User.username == c.username)):
        raise HTTPException(409, "username taken")
    db.add(User(username=c.username, password_hash=hash_password(c.password), role="citizen"))
    return {"status": "created"}
