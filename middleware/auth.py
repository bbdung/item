from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from jose import JWTError

from security.jwt import get_current_user


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path.startswith("/login"):
            return await call_next(request)

        try:
            get_current_user(request)  # chỉ để validate token
        except JWTError:
            return RedirectResponse("/login")
        except HTTPException:
            return RedirectResponse("/login")

        return await call_next(request)
