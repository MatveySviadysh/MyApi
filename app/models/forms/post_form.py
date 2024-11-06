from typing import Optional
from pydantic import BaseModel
from utils.classes import PostBase

class PostCreate(PostBase):
    author_id: int

    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None

    class Config:
        orm_mode = True