from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from models.user import User
from security.jwt import create_token

router = APIRouter()


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(401, "Invalid credentials")

    token = create_token(username)
    response = RedirectResponse("/items", status_code=302)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return response
