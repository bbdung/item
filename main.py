import datetime

from jose import jwt
import psycopg2
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, Form
from jose import JWTError
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates

SECRET_KEY = "secret123"
ALGORITHM = "HS256"
app = FastAPI()

templates = Jinja2Templates(directory="templates")

conn = psycopg2.connect(host="localhost",
                        port="5432",
                        database="postgres",
                        user="dungbb",
                        password="123456")

conn.autocommit = True


def create_token(username: str):
    payload = {
        "sub": username,
        "iat": datetime.datetime.now(datetime.UTC),
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    cur = conn.cursor()
    cur.execute(
        "SELECT password FROM users WHERE user_name=%s",
        (username,)
    )
    row = cur.fetchone()

    if not row or row[0] != password:
        raise HTTPException(401, "Invalid credentials")

    token = create_token(username)
    resp = RedirectResponse("/items", status_code=302)
    resp.set_cookie("access_token", token, httponly=True)
    return resp


@app.get("/items", response_class=HTMLResponse)
def list_items(request: Request, user=Depends(get_current_user)):
    cur = conn.cursor()
    cur.execute(
        "SELECT item_id, item_name FROM items"
    )
    items = cur.fetchall()

    return templates.TemplateResponse(
        "items.html",
        {
            "request": request,
            "items": items,
            "user": user
        }
    )


@app.post("/items")
def add_item(
        name: str = Form(...),
):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO items (item_name) VALUES (%s) RETURNING item_id, item_name",
        (name,)
    )
    item = cur.fetchone()

    return JSONResponse({
        "id": item[0],
        "name": item[1]
    })


uvicorn.run(app)
