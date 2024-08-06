import os
import string
import json

import aiofiles
import random
import motor.motor_asyncio
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{os.getenv("MONGODB_USERNAME", "root")}:{os.getenv("MONGODB_PASSWORD", "<example>")}@{os.getenv("MONGODB_HOST", "localhost")}:{os.getenv("MONGODB_PORT", 27017)}/')
client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://root:example@127.0.0.1:27017/')


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


@app.post("/")
async def get_url(url: Annotated[str, Form()]):
    short_url = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
    #
    # async with aiofiles.open('filename', mode='r') as f:
    #     contents = await f.read()
    #
    # db_dict = json.loads(contents)
    # db_dict[short_url] = url
    #
    # async with aiofiles.open('filename', mode='w') as f:
    #     await f.write(json.dumps(db_dict))
    new_doc = {"short_url": short_url, "long_url": url}
    await client["url_shortener"]["urls"].insert_one(new_doc)
    return {"result": short_url}


@app.get("/{short_url}")
async def say_hello(short_url: str):
    url_document = await client["url_shortener"]["urls"].find_one({"short_url": short_url})
    # await client.url_shortener.urls тоже самое
    res_url = url_document["long_url"]
    # async with aiofiles.open('filename', mode='r') as f:
    #     contents = await f.read()
    # db_dict = json.loads(contents)
    # url = db_dict[short_url]

    # hits_counter = url_document.get("hits_counter", 0)
    # url_document["hits_counter"] = hits_counter + 1
    url_document["hits_counter"] = url_document.get("hits_counter", 0) + 1
    await client["url_shortener"]["urls"].replace_one({"_id": url_document["_id"]}, url_document)
    return RedirectResponse(res_url)



# {"hits_counter": hits_counter + 1}