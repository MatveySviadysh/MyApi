from utils.classes import UserBase

class User(UserBase):
    id: int

    class Config:
        orm_mode = True