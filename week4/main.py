from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.post("/signin")
async def signin(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    if email == "" or password == "":
        return RedirectResponse(
            url="/ohoh?msg=請輸入信箱和密碼",
            status_code=307
        )
    
    if email in USER_DATABASE:
        if password == USER_DATABASE[email]:
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
    return templates.TemplateResponse(
        request=request,
        name="member.html"
    )

@app.get("/ohoh")
async def ohoh(request: Request, msg: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="ohoh.html",
        context={"msg": msg}
    )