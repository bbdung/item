from fastapi import APIRouter, Form, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from db.session import get_db
from security.security import create_token
from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/")
def login(username: str = Form(...),
          password: str = Form(...),
          db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(401, "Invalid credentials")

    token = create_token(username)
    resp = RedirectResponse("/items", status_code=302)
    resp.set_cookie("access_token", token, httponly=True)
    return resp
