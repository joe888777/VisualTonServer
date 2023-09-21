from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import createHtml
from utils.utils_api import filterTX 
from getData import *


app = FastAPI()

origins = ['http://localhost:3000', 'https://localhost:3000','*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/filteredNodes/")
async def getFilteredNodes(amount: int):
    data = getData()
    a = filterTX(data, amount)
    return a

@app.get("/graph/")
async def getGraph():
    html = ShortData()
    return JSONResponse(content=html, status_code=200)

@app.get("/")
async def root():
    return {"message": "Hello World"}

import json
@app.get("/mock/")
async def getMock():
    with open('output.json','r') as file :
        data = json.load(file)
        return data

from getData import getAddressTable
@app.get("/node_info/")
async def AddressTable():
    return getAddressTable()
