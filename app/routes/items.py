from fastapi import APIRouter, Path, Query
from typing import List, Dict, Optional, Annotated
from models.forms.post_form import PostCreate
from models.post_model import Post
from services.post_services import find_post_by_id, get_all_posts, posts
from services.user_services import users
from models.forms.post_form import PostCreate
from fastapi import HTTPException
post_router = APIRouter()


@post_router.get("/items", response_model=List[Post])
async def items() -> List[Post]:
    return get_all_posts()

@post_router.get("/items/{id}", response_model=Post)
async def get_item(id: Annotated[
        int, 
            Path(
            ..., 
            tittle='int сдесь указываетьс id  поста', 
            ge = 1, 
            lt= 100)
        ]) -> Post:
    post_data = await find_post_by_id(id)
    return Post(**post_data) # type: ignore

@post_router.get("/search", response_model=Post)
async def search_post(post_id: Annotated[
            Optional[int],
            Query(title='ID of the post to search for', ge=1, le=50)
        ]
    ) -> Dict[str, Optional[Post]]:
    if post_id is not None:
        post_data = await find_post_by_id(post_id)
        return Post(**post_data) # type: ignore
    else:
        return {"data": None}
    
@post_router.post("/items/create") 
async def create_post(post: PostCreate) -> Post:
    creator = next((user for user in users if user["id"] == post.creater_id), None)
    if not creator:
        raise HTTPException(status_code=404,detail="user not found")
    
    new_post_id = len(posts) + 1
    new_post_title = post.title
    new_post_text = post.body
    
    new_post = {
        'id': new_post_id,
        'author': creator,
        'title': new_post_title,
        'text': new_post_text
    }
    posts.append(new_post)
    return Post(**new_post)