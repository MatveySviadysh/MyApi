from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    body: str
    creater_id: int