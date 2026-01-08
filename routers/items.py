from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates

from dependencies import get_db
from service.itemService import get_items, create_item

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def list_items(request: Request, db: Session = Depends(get_db)):
    items = get_items(db)
    user = request.state.user
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
    item = create_item(db, name)
    return JSONResponse(
        {
            "id": item.id,
            "name": item.name,
        }
    )
