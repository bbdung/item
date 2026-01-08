from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates

from db.session import get_db
from models.item import Item
from security.security import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def list_items(request: Request, user=Depends(get_current_user),
               db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return templates.TemplateResponse(
        "items.html",
        {
            "request": request,
            "items": items,
            "user": user
        }
    )


@router.post("/")
def add_item(name: str = Form(...), db: Session = Depends(get_db)):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)

    return JSONResponse({
        "id": item[0],
        "name": item[1]
    })
