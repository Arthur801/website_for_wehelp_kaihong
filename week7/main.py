from typing import Annotated
from pydantic import BaseModel

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

class messageData(BaseModel):
    id:int
    name:str
    content:str
    self:bool

class responseMessageCreate(BaseModel):
    ok:bool
    data:list[messageData]

class requestMessageCreate(BaseModel):
    content:str

# 建立fastapi server
app=FastAPI()

# 連結靜態資料與建立確認網站是否登入的middleware
app.mount("/static", StaticFiles(directory="static"), name="static") # 必須要先cd week6之後才不會出問題
app.add_middleware(SessionMiddleware, secret_key="gjapsfu1")
# 取得jinja2模板資料夾（html)
templates = Jinja2Templates(directory="templates") # 同第16行

# 建立db與tables
websiteDB = mysql.connector.connect(
    host="localhost",
    user="test",
    password="Abcd1234!"
)
mycursor = websiteDB.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS website")
mycursor.execute("USE website")
# member table
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
# 留言table
mycursor.execute(
    """
    CREATE TABLE IF NOT EXISTS message(
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        member_id INT UNSIGNED NOT NULL, 
        CONSTRAINT fk_id FOREIGN KEY (member_id) REFERENCES member(id),
        content MEDIUMTEXT NOT NULL,
        like_count INT UNSIGNED NOT NULL DEFAULT 0,
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
    # 後端再次檢查是否為空
    if email == "" or password == "" or userName == "":
        return RedirectResponse(
            url="/ohoh?msg=請輸入姓名、電子郵件與密碼",
            status_code=303
        )
    # 建一個signup專用的cursor避免共用global的cursor，檢查user email 帳號是否已存在，是則導向錯誤頁面，error msg = "重複的電子郵件"
    signupCursor = websiteDB.cursor()
    signupCursor.execute("SELECT * FROM member WHERE email = %s LIMIT 1", (email, )) # 必須是list, tuple或dict
    if signupCursor.fetchone() is not None:
        signupCursor.close()
        return RedirectResponse(
            url="/ohoh?msg=重複的電子郵件",
            status_code=303
        )
    # 若資料庫中member不存在相同的email，成功註冊，將資料輸入資料庫並導回首頁，使用%s傳入引數
    else:
        signupCursor.execute("INSERT INTO member (name, email, password) VALUE (%s, %s, %s)", (userName, email, password))
        websiteDB.commit()
        signupCursor.close()
        return RedirectResponse(
            url="/",
            status_code=303
        )
# 首頁登入
@app.post("/login")
async def login(request: Request,
                email: Annotated[str, Form()],
                password: Annotated[str, Form()]):
    # 前端檢查登入資料是否為空，後端不檢查
    # 建一個登入專用cursor，檢查登入資料與資料庫中的member email 和password 是否吻合，是則導向member page，否則導向error page
    loginCursor = websiteDB.cursor()
    loginCursor.execute("SELECT * FROM member WHERE email = %s AND password = %s LIMIT 1", (email, password))
    userData = loginCursor.fetchone()
    if userData is not None:
        # session存member ID 和姓名
        userID, userName, userEmail = userData[0], userData[1], userData[2]
        request.session["userID"] = userID
        request.session["userName"] = userName
        request.session["userEmail"] = userEmail
        loginCursor.close()

        return RedirectResponse(
            url="/member",
            status_code=303
        )
    else:
        loginCursor.close()
        return RedirectResponse(
            url="/ohoh?msg=電子郵件或密碼錯誤",
            status_code=303
        )

# 接入使用者頁面
@app.get("/member")
async def member(request: Request,):
    # 進入使用者頁面，先用middleware檢查登入狀態
    if request.session.get("userName") is not None:
        return templates.TemplateResponse(
            request=request,
            name="member.html",
            context={"userName": request.session.get("userName")}
        )
    # 若未登入則導向首頁
    else:
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

# 在使用者頁面選擇登出，將session中的資料變成空值，避免使用者能在未登入的狀態下進入使用者頁面
@app.get("/logout")
async def logout(request: Request):
    request.session["userID"] = None
    request.session["userName"] = None
    request.session["userEmail"] = None
    return RedirectResponse(
        url="/"
    )

# POST /api/message
@app.post("/api/message")
async def sendMessage(request: Request,message: requestMessageCreate):
    userName,userID = request.session.get("userName"), request.session.get("userID")
    # 檢查登入狀態、message content，有問題回傳{"error":Ture}
    if not userName or not userID:
        return { "error": True }
    content = message.content
    if not message or not content:
        return { "error": True }

    # 若登入狀態與message content 都沒有問題，建立cursor，將message存到websiteDB裡的table message
    messageCursor = None
    try:
        messageCursor = websiteDB.cursor()
        messageCursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s);", (userID, content))
        websiteDB.commit()
        return { "ok": True }
    except Exception:
        websiteDB.rollback()
        return { "error": True }
    finally:
        if messageCursor is not None:
            messageCursor.close()
    
# GET /api/message
@app.get("/api/message")
async def getMessage(request: Request):
    currentUserName, currentUserID = request.session.get("userName"), request.session.get("userID")
    # 檢查登入狀態
    if not currentUserName or not currentUserID:
        return { "error": True }
    
    # 建立cursor，取出message
    messageCursor = None
    try:
        messageCursor = websiteDB.cursor()
        messageCursor.execute("SELECT message.*, member.name FROM message INNER JOIN member ON message.member_id = member.id ORDER BY message.time DESC")
        messages = messageCursor.fetchall()
        data = []
        for msg in messages:
            data.append({
                "id": msg[0],
                "name": msg[5],
                "content": msg[2],
                "self": currentUserID == msg[1]
            })

        return { "ok": True, "data": data }
    except Exception:
        return { "error": True }
    finally:
        if messageCursor is not None:
            messageCursor.close()
    
# DELETE /api/message
@app.delete("/api/message/{messageID}")
async def delMessage(request: Request, messageID: str):
    currentUserID = request.session.get("userID")
    # 檢查登入狀態
    if not currentUserID:
        return { "error": True }
    
    # 建立cursor，確認資料庫裡有messageID符合的message，刪除該message，否則回傳error
    messageCursor = None
    try:
        messageCursor = websiteDB.cursor()
        messageCursor.execute("SELECT * FROM message WHERE message.id = %s", (messageID, ))
        messageToDel = messageCursor.fetchone()
        if not messageToDel:
            return { "error": True }
        if messageToDel[1] != currentUserID:
            return { "error": True }
        messageCursor.execute("DELETE FROM message WHERE id = %s AND message.member_id = %s", (messageID, currentUserID))
        websiteDB.commit()
        return { "ok": True }
    except Exception:
        return { "error": True }
    finally:
        if messageCursor is not None:
            messageCursor.close()

# api token
@app.put("/api/token")
async def createToken(request: Request):
    pass