import uvicorn
from fastapi import FastAPI
from starlette.templating import Jinja2Templates

from service.loginService import router as login_router
from service.itemService import router as item_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(item_router, prefix="/items", tags=["items"])
uvicorn.run(app)
