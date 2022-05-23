from configparser import ConfigParser
from typing import Union

from fastapi import FastAPI

from databases.grouper import Database
from utils.structures import Databases


config = ConfigParser()
config.read('config.ini')

app = FastAPI()
app.db = Database((config['database']['DatabaseChoice']), config['database']['Uri']).db

app.db['test'].insert({'sxz': 'test'})
app.db['test'].delete('sxz')
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None): # q is optional and a query string like ?q=abc
    return {"item_id": item_id, "q": q}
