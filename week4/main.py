from fastapi import FastAPI
from jinja2 import Template
app=FastAPI()

@app.get("/")
def index():
    return [100, 200, 300]