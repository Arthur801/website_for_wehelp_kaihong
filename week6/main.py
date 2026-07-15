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
app.mount("/static", StaticFiles(directory="static"), name="static") # 必須要先cd week6之後才不會出問題
app.add_middleware(SessionMiddleware, secret_key="gjapsfu1")
# 取得jinja2模板資料夾（html)
templates = Jinja2Templates(directory="templates") # 同第16行

# 模擬使用者帳號資料庫
# USER_DATABASE = {
#     "abc@abc.com" : "abc"
# }
# 建立db與tables
websiteDB = mysql.connector.connect(
    host="localhost",
    user="Test",
    password="abcd1234!"
)
mycursor = websiteDB.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS website")
mycursor.execute("USE website")
mycursor.execute(
    """
    CREATE TABLE IF NOT EXISTS member (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name varchar(255) NOT NULL,
        email varchar(255) NOT NULL UNIQUE,
        password varchar(255) NOT NULL,
        follower_count INT UNSIGNED NOT NULL DEFAULT 0,
        time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
)
mycursor.close()


# 連進首頁
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

# 首頁註冊
@app.post("/signup")
async def signup(request: Request, userName: Annotated[str, Form()],
                email: Annotated[str, Form()],
                password: Annotated[str, Form()]):
    # 輸入包含空值，在前端檢查，後端不寫檢查程式碼
    # 建一個signup專用的cursor避免共用global的cursor，檢查user email 帳號是否已存在，是則導向錯誤頁面，error msg = "重複的電子郵件"
    signupCursor = websiteDB.cursor()
    signupCursor.execute("SELECT * FROM member WHERE email = %s LIMIT 1", (email, )) # 必須是list, tuple或dict
    if signupCursor.fetchone() is not None:
        signupCursor.close()
        return RedirectResponse(
            url="/ohoh?msg=重複的電子郵件",
            status_code=303
        )
    # 若資料庫中member不存在相同的email，成功註冊，將資料輸入資料庫，導回首頁並將session變成已登入狀態，使用%s傳入引數
    else:
        signupCursor.execute("INSERT INTO member (name, email, password) VALUE (%s, %s, %s)", (userName, email, password))
        websiteDB.commit()
        signupCursor.close()
        # 這邊可能需要改成存是哪一個user登入的資訊
        request.session["LOGGED-IN"] = True
        return RedirectResponse(
            url="/",
            status_code=303
        )
# 首頁登入
@app.post("/login")
async def login(request: Request,
                email: Annotated[str, Form()] = "",
                password: Annotated[str, Form()] = ""):
    
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