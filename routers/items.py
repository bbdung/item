from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates

from dependencies import get_db
from security.jwt import get_current_user
from service.itemService import get_items, create_item

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def list_items(request: Request,
               user=Depends(get_current_user),
               db: Session = Depends(get_db)
               ):
    items = get_items(db)
    return templates.TemplateResponse(
        "items.html",
        {
            "request": request,
            "items": items,
            "user" : user
        }
    )


@router.post("/")
def add_item(name: str = Form(...), db: Session = Depends(get_db)):
    item = create_item(db, name)
    return JSONResponse(
        {
            "id": item.id,
            "name": item.name,
        }
    )
