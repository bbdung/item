from fastapi import Depends, Form, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from core.security import get_current_user
from dependencies import get_db
from models.item import Item

templates = Jinja2Templates(directory="templates")


def get_list_items(request: Request, user=Depends(get_current_user),
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


def add_new_item(name: str = Form(...), db: Session = Depends(get_db)):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)

    return JSONResponse({
        "id": item.id,
        "name": item.name,
    })
