import uvicorn
from fastapi import FastAPI

from middleware.auth import AuthMiddleware
from routers.users import router as login_router
from routers.items import router as item_router

app = FastAPI()

app.add_middleware(AuthMiddleware)

app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(item_router, prefix="/items", tags=["items"])

uvicorn.run(app)
