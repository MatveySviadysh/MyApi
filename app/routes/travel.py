from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database.models import Travel
from models.travel_model import TravelCreate, TravelResponse
from utils.helpers import get_db

travel_router = APIRouter()

@travel_router.post('/travel/create',  tags=["Travel"], summary="Создает новое путешествие",response_model=TravelResponse)
async def create_travel(travel: TravelCreate, db: Session = Depends(get_db)) -> TravelResponse:
    """
    Создает новое путешествие.

    - **travel**: Объект данных о путешествии для создания, включает:
        - **name**: Название путешествия
        - **description**: Описание путешествия
        - **price**: Цена путешествия
        - **duration**: Продолжительность путешествия
        - **start_date**: Дата начала
        - **end_date**: Дата окончания
        - **image_url**: URL изображения путешествия
        - **city_id**: ID города
        - **guide_id**: (необязательный) ID гида

    Возвращает созданный объект путешествия.
    """
    existing_travel = db.query(Travel).filter(Travel.name == travel.name).first()
    if existing_travel:
        raise HTTPException(status_code=400, detail="Travel with this name already exists.")
    
    new_travel = Travel(
        name=travel.name,
        description=travel.description,
        price=travel.price,
        duration=travel.duration,
        start_date=travel.start_date,
        end_date=travel.end_date,
        image_url=travel.image_url,
        city_id=travel.city_id,
        guide_id=travel.guide_id if hasattr(travel, 'guide_id') else None
    )
    db.add(new_travel)
    db.commit()
    db.refresh(new_travel)
    return new_travel


@travel_router.get('/treves',  tags=["Travel"], summary="Получает список всех путешествий",response_model=list[TravelResponse])
async def get_treves(db: Session = Depends(get_db)) -> list[Travel]:
    """
    Получает список всех путешествий.

    Возвращает список объектов путешествий с загруженными связями с городами.
    """
    travels = db.query(Travel).options(joinedload(Travel.city)).all()
    return travels


@travel_router.get('/travel/{id}',  tags=["Travel"], summary="Ищет путешествие по ID",response_model=TravelResponse)
async def search_travel(id: int, db: Session = Depends(get_db)) -> Travel:
    """
    Ищет путешествие по ID.

    - **id**: ID путешествия для поиска.

    Если путешествие не найдено, возвращает ошибку 404.
    """
    travel = db.query(Travel).options(joinedload(Travel.city), joinedload(Travel.guide)).filter(Travel.id == id).first()
    if travel is None:
        raise HTTPException(status_code=404, detail="Travel not found")
    return travel


@travel_router.delete('/travel/{id}', tags=["Travel"], summary="Удаляет путешествие по ID", response_model=dict)
async def delete_travel(id: int, db: Session = Depends(get_db)) -> dict:
    """
    Удаляет путешествие по ID.

    - **id**: ID удаляемого путешествия.

    Возвращает сообщение об успешном удалении.
    """
    travel = db.query(Travel).options(joinedload(Travel.city), joinedload(Travel.guide)).filter(Travel.id == id).first()
    if travel is None:
        raise HTTPException(status_code=404, detail="Travel not found")
    db.delete(travel)
    db.commit()
    return {"message": "Travel deleted successfully"}


@travel_router.put('/travel/{id}', tags=["Travel"], summary="Обновляет информацию о путешествии", response_model=TravelResponse)
async def update_travel(id: int, travel: TravelCreate, db: Session = Depends(get_db)) -> TravelResponse:
    """
    Обновляет информацию о путешествии.

    - **id**: ID путешествия для обновления.
    - **travel**: Объект TravelCreate с обновляемыми данными, включает:
        - **name**: Название путешествия
        - **description**: Описание путешествия
        - **price**: Цена путешествия
        - **duration**: Продолжительность путешествия
        - **start_date**: Дата начала
        - **end_date**: Дата окончания
        - **image_url**: URL изображения путешествия
        - **city_id**: ID города
        - **guide_id**: (необязательный) ID гида

    Возвращает обновленный объект путешествия.
    """
    db_travel = db.query(Travel).options(joinedload(Travel.city), joinedload(Travel.guide)).filter(Travel.id == id).first()
    if db_travel is None:
        raise HTTPException(status_code=404, detail="Travel not found")

    db_travel.name = travel.name # type: ignore
    db_travel.description = travel.description # type: ignore
    db_travel.price = travel.price # type: ignore
    db_travel.duration = travel.duration # type: ignore
    db_travel.start_date = travel.start_date # type: ignore
    db_travel.end_date = travel.end_date # type: ignore
    db_travel.image_url = travel.image_url # type: ignore
    if travel.city_id:
        db_travel.city_id = travel.city_id # type: ignore
    if travel.guide_id is not None:
        db_travel.guide_id = travel.guide_id # type: ignore

    db.commit()
    db.refresh(db_travel)
    return db_travel
