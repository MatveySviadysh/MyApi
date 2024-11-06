from pydantic import BaseModel, Field
from typing import Annotated

class UserCreate(BaseModel):
    name: Annotated[
        str,
        Field(...,title="name the new user",max_length=20,min_length=5)
    ]
    age: Annotated[
        int,
        Field(..., title="Age of the new user", ge=5, le=120)
    ]