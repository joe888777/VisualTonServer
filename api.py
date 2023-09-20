from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import createHtml
from utils.utils_api import filterTX

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/filteredNodes/")
async def getFilteredNodes(amount: int):
    data = createHtml.html_to_text()
    a = filterTX(data, amount)
    return a

@app.get("/graph/")
async def getGraph():
    html,data = createHtml.html_to_text()
    return HTMLResponse(content=html, status_code=200)

@app.get("/")
async def root():
    return {"message": "Hello World"}

