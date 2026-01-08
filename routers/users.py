from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from dependencies import get_db
from service.loginService import authenticate_user

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/", )
def login(username: str = Form(...),
          password: str = Form(...),
          db: Session = Depends(get_db)):
    return authenticate_user(username, password, db)
