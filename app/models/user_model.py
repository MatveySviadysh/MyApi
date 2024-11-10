from utils.classes import UserBase

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True