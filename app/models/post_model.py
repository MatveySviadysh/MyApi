from pydantic import BaseModel
from .user_model import User

class Post(BaseModel):
    id: int
    title: str
    text: str 
    author: User