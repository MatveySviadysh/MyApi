from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from models.forms.user_form import UserCreate
from models.user_model import User
from utils.helpers import get_db
from database.models import User as UserModel
from typing import Annotated

user_router = APIRouter()

@user_router.post('/user/create', response_model=User)
async def create_user(
        user: Annotated[UserCreate, Body(..., example={"name": "dasha", "age": 88})],
        db: Session = Depends(get_db)
    ) -> User:
    new_user = UserModel(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return User(id=new_user.id, name=new_user.name, age=new_user.age)