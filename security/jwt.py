import datetime

from fastapi import HTTPException
from jose import JWTError, jwt
from starlette.requests import Request

from security.keys import PRIVATE_KEY
from security.keys import PUBLIC_KEY

ALGORITHM = "RS256"


def create_token(username: str):
    payload = {
        "sub": username,
        "iat": datetime.datetime.now(datetime.UTC),
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
    }

    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM]
        )
        return payload["sub"]

    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
