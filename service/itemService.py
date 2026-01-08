from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from models.item import Item

templates = Jinja2Templates(directory="templates")


def get_items(db: Session):
    items = db.query(Item).all()
    return items


def create_item(db: Session, name: str):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
