from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    age: int


class PostBase(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None