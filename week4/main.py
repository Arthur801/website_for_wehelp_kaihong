from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware

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
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()], request: Request):
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
    if request.session["LOGGED-IN"] == True:
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
