from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware
import mysql.connector


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
# 建立db與tables
pass

# 連進首頁
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

# 首頁註冊
@app.post("/signup")
async def signup(requese: Request, userName: Annotated[str, Form()] = "", email: Annotated[str, Form()] = "", password: Annotated[str, Form()] = ""):
    # 輸入包含空值，在前端檢查，後端不寫檢查程式碼
    # user email 帳號已存在，導向錯誤頁面，error msg = "重複的電子郵件"
    pass
    # 成功註冊，將資料輸入資料庫，導回首頁並將session變成已登入狀態
    pass

# 首頁登入
@app.post("/login")
async def login(request: Request, email: Annotated[str, Form()] = "", password: Annotated[str, Form()] = ""):
    if email == "" or password == "":
        # 為填入資料導向錯誤頁面，並傳入錯誤訊息
        return RedirectResponse(
            url="/ohoh?msg=請輸入信箱和密碼",
            status_code=303
        )
    
    if email in USER_DATABASE:
        if password == USER_DATABASE[email]:
            request.session["LOGGED-IN"] = True
            # 判斷登入成功後導向使用者頁面
            return RedirectResponse(
                url="/member",
                status_code=303
            )
    return RedirectResponse(
        # 登入資料輸入錯誤後導向錯誤頁面，並傳入錯誤訊息
        url="/ohoh?msg=信箱或密碼輸入錯誤",
        status_code=303
    )

# 接入使用者頁面
@app.get("/member")
async def member(request: Request):
    # 進入使用者頁面，先用middleware檢查登入狀態
    if request.session.get("LOGGED-IN", True):
        return templates.TemplateResponse(
            request=request,
            name="member.html"
        )
    # 若未登入則導向首頁
    return RedirectResponse(
        url="/",
        status_code=303
    )

# 接入錯誤頁面
@app.get("/ohoh")
async def ohoh(request: Request, msg: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="ohoh.html",
        context={"msg": msg}
    )

# 在使用者頁面選擇登出，將登入狀態設為false，避免使用者能在未登入的狀態下進入使用者頁面
@app.get("/logout")
async def logout(request: Request):
    request.session["LOGGED-IN"] = False
    return RedirectResponse(
        url="/"
    )