from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from core.security import create_token
from dependencies import get_db
from models.user import User

router = APIRouter()


def authenticate_user(username: str = Form(...),
                      password: str = Form(...),
                      db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(401, "Invalid credentials")

    token = create_token(username)
    resp = RedirectResponse("/items", status_code=302)
    resp.set_cookie("access_token", token, httponly=True)
    return resp
