from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

from security.jwt import get_current_user


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if (
                request.url.path.startswith("/login")
                or request.url.path.startswith("/static")
        ):
            return await call_next(request)

        try:
            user = get_current_user(request)
            request.state.user = user

        except HTTPException:
            return RedirectResponse("/login", status_code=302)

        return await call_next(request)
