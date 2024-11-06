from fastapi import HTTPException
from typing import List, Dict
from models.post_model import Post

posts = [
    {"id": 1, "title": "кошки", "text": "они бегают и мяукают"},
    {"id": 2, "title": "сбежали медведи", "text": "из-заопврка пропали медведи что же делать"},
    {"id": 3, "title": "пингвинчики", "text": "так заяви репер благо вайт"},
]

async def find_post_by_id(post_id: int) -> Dict[str, str]:
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail='такой пост не обнаружен')

def get_all_posts() -> List[Post]:
    return [Post(id=post["id"], title=post["title"], text=post["text"]) for post in posts]
