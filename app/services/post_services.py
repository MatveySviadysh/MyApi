from fastapi import HTTPException
from typing import List, Dict
from models.post_model import Post
from models.user_model import User
from services.user_services import users

posts = [
    {"id": 1, "title": "кошки", "text": "они бегают и мяукают",'author': users[0]},
    {"id": 2, "title": "сбежали медведи", "text": "из-заопврка пропали медведи что же делать",'author': users[1]},
    {"id": 3, "title": "пингвинчики", "text": "так заяви репер благо вайт",'author': users[2]},
]

async def find_post_by_id(post_id: int) -> Dict[str, str]:
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail='такой пост не обнаружен')

def get_all_posts() -> List[Post]:
    return [
        Post(
            id=post["id"],
            title=post["title"],
            text=post["text"],
            author=User(**post["author"])
        ) for post in posts
    ]
