from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware

import urllib.request as request
import json

with request.urlopen("https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch") as responseCH:
    dataCH = json.load(responseCH)

with request.urlopen("https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en") as responseEN:
    dataEN = json.load(responseEN)

hotelsListCH = dataCH["list"]
hotelsListEN = dataEN["list"]

# 需要透過"_id"比對並取得hotelsListCH和hotelListEN中相同旅館的資料
# 把hotelsListEN做成字典, key: _id, value: {"hotelName":"hn", "addressEN":"addr"}
hotelsDict = {}
for hotel in hotelsListEN:
    hotelsDict[hotel['_id']] = {"hotelNameEN":hotel["hotel name"]}

# 把hotelsListCH的資料也加入字典
for hotel in hotelsListCH:
    hotelsDict[hotel["_id"]].update({"hotelNameCH":hotel["旅宿名稱"], "phone":hotel["電話或手機號碼"]})

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

# 接入旅館頁面，使用抓下來的資料進行比對，回傳對應的結果
@app.get("/hotel/{hotelId}")
async def hotel_search(request: Request, hotelId: int):
    if hotelId not in hotelsDict:
        context = {"hotel_name_ch":"查詢不到相關資料"}
        return templates.TemplateResponse(
            request=request,
            name="hotel.html",
            context=context
        )
    # 用context傳遞資料給html頁面
    context = {
        "hotel_name_ch" : hotelsDict[hotelId]["hotelNameCH"],
        "hotel_name_en" : hotelsDict[hotelId]["hotelNameEN"],
        "hotel_phone" : hotelsDict[hotelId]["phone"]
    }
    return templates.TemplateResponse(
        request=request,
        name="hotel.html",
        context=context
    )