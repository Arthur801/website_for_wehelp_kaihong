from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware


# 建立fastapi server
app=FastAPI()

# 連結靜態資料與建立確認網站是否登入的middleware
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="gjapsfu1")
# 取得jinja2模板資料夾（html)
templates = Jinja2Templates(directory="templates")

# 模擬使用者帳號資料庫
USER_DATABASE = {
    "abc@abc.com" : "abc"
}

# 連進首頁
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )