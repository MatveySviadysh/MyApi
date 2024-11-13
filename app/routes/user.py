from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user_model import User, UserCreate, UserResponse
from utils.helpers import get_db
from database.models import User as UserModel
from typing import Annotated, List

user_router = APIRouter()

fake_session_store = {}

@user_router.post('/user/create', tags=["User"], summary="Создает нового пользователя", response_model=UserResponse)
async def create_user(
        user: Annotated[UserCreate, Body(..., example={"name": "dasha", "age": 88})],
        db: Session = Depends(get_db)
    ) -> UserResponse:
    """
    Создает нового пользователя.
    
    - **name**: Имя пользователя.
    - **age**: Возраст пользователя.
    
    Возвращает созданный объект пользователя.
    """
    new_user = UserModel(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse(id=new_user.id, name=new_user.name, age=new_user.age) # type: ignore

@user_router.get('/user/{id}',  tags=["User"], summary="Получает информацию о пользователе по его ID",response_model=UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)) -> UserResponse:
    """
    Получает информацию о пользователе по его ID.
    
    - **id**: ID пользователя.
    
    Если пользователь не найден, возвращает ошибку 404.
    """
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user.id, name=user.name, age=user.age) # type: ignore

@user_router.get('/users',  tags=["User"], summary="Получает список всех пользователей",response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    """
    Получает список всех пользователей.
    
    Возвращает список объектов пользователей.
    """
    users = db.query(UserModel).all()
    return [UserResponse(id=user.id, name=user.name, age=user.age) for user in users] # type: ignore

@user_router.delete('/user/{user_id}', tags=["User"], summary="Удаляет пользователя по его ID", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Удаляет пользователя по его ID.
    
    - **user_id**: ID удаляемого пользователя.
    
    Возвращает сообщение об успешном удалении.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@user_router.post('/user/login', tags=["User"], summary="Логин пользователя")
async def login(user: Annotated[UserCreate, Body(..., example={"name": "dasha", "age": 88})], db: Session = Depends(get_db)):
    """
    Логин пользователя.

    - **name**: Имя пользователя.
    - **age**: Возраст пользователя.

    Возвращает сообщение об успешном логине или ошибку.
    """
    db_user = db.query(UserModel).filter(UserModel.name == user.name, UserModel.age == user.age).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_token = f"session-{db_user.id}"
    fake_session_store[session_token] = db_user.id
    return {"message": "Login successful", "session_token": session_token}


@user_router.post('/user/logout', tags=["User"], summary="Выход из аккаунта")
async def logout(session_token: str = Body(...)):
    """
    Выход из аккаунта.

    - **session_token**: Токен сессии.

    Возвращает сообщение об успешном выходе.
    """
    if session_token in fake_session_store:
        del fake_session_store[session_token]
        return {"message": "Logout successful"}
    raise HTTPException(status_code=404, detail="Session token not found")