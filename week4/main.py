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

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="gjapsfu1")

templates = Jinja2Templates(directory="templates")

USER_DATABASE = {
    "abc@abc.com" : "abc"
}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.post("/login")
async def login(request: Request, email: Annotated[str, Form()] = "", password: Annotated[str, Form()] = ""):
    if email == "" or password == "":
        return RedirectResponse(
            url="/ohoh?msg=請輸入信箱和密碼",
            status_code=303
        )
    
    if email in USER_DATABASE:
        if password == USER_DATABASE[email]:
            request.session["LOGGED-IN"] = True
            return RedirectResponse(
                url="/member",
                status_code=303
            )
    return RedirectResponse(
        url="/ohoh?msg=信箱或密碼輸入錯誤",
        status_code=303
    )
    
@app.get("/member")
async def member(request: Request):
    if request.session.get("LOGGED-IN", True):
        return templates.TemplateResponse(
            request=request,
            name="member.html"
        )
    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.get("/ohoh")
async def ohoh(request: Request, msg: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="ohoh.html",
        context={"msg": msg}
    )

@app.get("/logout")
async def logout(request: Request):
    request.session["LOGGED-IN"] = False
    return RedirectResponse(
        url="/"
    )

@app.get("/hotel/{hotelId}")
async def hotel_search(request: Request, hotelId: int):
    if hotelId not in hotelsDict:
        context = {"hotel_name_ch":"查詢不到相關資料"}
        return templates.TemplateResponse(
            request=request,
            name="hotel.html",
            context=context
        )
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