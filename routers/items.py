from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from core.security import get_current_user
from dependencies import get_db
from service.itemService import get_list_items, add_new_item

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def list_items(request: Request,
               user=Depends(get_current_user),
               db: Session = Depends(get_db)):
    return get_list_items(request, user, db)


@router.post("/")
def add_item(name: str = Form(...), db: Session = Depends(get_db)):
    return add_new_item(name, db)
