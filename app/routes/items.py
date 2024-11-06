from fastapi import APIRouter
from typing import List, Dict, Optional
from models.post_model import Post
from services.services import find_post_by_id, get_all_posts

router = APIRouter()

@router.get("/")
async def home() -> Dict[str, str]:
    return {"data": "message"}

@router.get("/contacts")
async def contacts() -> int:
    return 375295773787

@router.get("/items", response_model=List[Post])
async def items() -> List[Post]:
    return get_all_posts()

@router.get("/items/{id}", response_model=Post)
async def get_item(id: int) -> Post:
    post_data = await find_post_by_id(id)
    return Post(**post_data) # type: ignore

@router.get("/search", response_model=Post)
async def search_post(post_id: Optional[int] = None) -> Dict[str, str]:
    if post_id is not None:
        post_data = await find_post_by_id(post_id)
        return Post(**post_data) # type: ignore
    else:
        return {"data": "not found post by id"}
