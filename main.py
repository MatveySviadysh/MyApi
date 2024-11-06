from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict

app = FastAPI()

@app.get("/")
async def home() -> Dict[str, str]:
    return {"data": "messge"}

@app.get("/contacts")
async def contacts() -> int:
    return 375295773787

posts = [
    {"id": "1", "title": "кошки", "text": "они бегают и мяукают"},
    {"id": "2", "title": "сбежали медведи", "text": "из-заопврка пропали медведи что же делать"},
    {"id": "3", "title": "пингвинчики", "text": "так заяви репер благо вайт"},
]

@app.get("/items")
async def items() -> List[Dict[str, str]]:
    return posts

async def find_post_by_id(posts, id: str) -> Dict[str, str]:
    for post in posts:
        if post['id'] == id:
            return post
    raise HTTPException(status_code=404, detail='такой пост не обнаружен')

@app.get("/items/{id}")
async def get_item(id: str) -> Dict[str, str]:
    return await find_post_by_id(posts, id)

@app.get("/search")
async def search_post(post_id: Optional[int] = None) -> Dict[str, str]:
    if post_id is not None:
        return await find_post_by_id(posts, str(post_id))
    else:
        return {"data": "not founded post by id"}