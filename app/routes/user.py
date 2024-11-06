from fastapi import APIRouter, Body
from models.forms.user_form import UserCreate
from models.user_model import User
from services.user_services import users
from typing import Annotated
user_router = APIRouter()

@user_router.post('/user/create')
async def create_user(user: Annotated[
        UserCreate,
        Body(...,example={
            "name": "dasha",  
            "age": 88
        })
    ]) -> User:
    new_user_id = len(users) + 1
    new_user_name = user.name
    new_user_age = user.age

    new_user = {
        'id': new_user_id,
        'name': new_user_name,
        'age': new_user_age,
    }
    users.append(new_user)
    return User(**new_user)