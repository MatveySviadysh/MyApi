from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.models import City, Travel
from models.city_model import CityCreate, CityResponse
from models.travel_model import TravelResponse
from utils.helpers import get_db

city_router = APIRouter()

@city_router.post("/city/create", response_model=CityResponse)
async def create_city(city: CityCreate, db: Session = Depends(get_db)) -> CityResponse:
    """
    Создает новый город.
    
    - **name**: Название города
    - **description**: Описание города
    - **image_url**: URL изображения города

    Возвращает созданный объект города.
    """
    existing_city = db.query(City).filter(City.name == city.name).first()
    if existing_city:
        raise HTTPException(status_code=400, detail="City with this name already exists.")
    db_city = City(
        name=city.name,
        description=city.description,
        image_url=city.image_url
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@city_router.get("/cities", response_model=list[CityResponse])
async def get_cities(db: Session = Depends(get_db)) -> list[City]:
    """
    Получает список всех городов.
    Возвращает список объектов городов.
    """
    cities = db.query(City).all()
    return cities


@city_router.get("/city", response_model=CityResponse)
async def search_city(
        id: int = Query(None, ge=1, le=50, description="ID города для поиска. Должен быть в пределах от 1 до 50."),
        filter: str = Query(None, description="Часть названия города для фильтрации.")
    , db: Session = Depends(get_db)) -> CityResponse:
    """
    Ищет город по ID или по фильтру.
    Вы можете передать либо `id`, либо `filter` для выполнения поиска.
    
    - **id**: ID города в базе данных.
    - **filter**: Строка для фильтрации городов по названию.

    Если город не найден, возвращает ошибку 404.
    """
    query = db.query(City)
    if id is not None:
        city = query.filter(City.id == id).first()
    else:
        city = None
    if filter:
        city = query.filter(City.name.ilike(f"%{filter}%")).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@city_router.delete("/city/{city_id}", response_model=dict)
async def delete_city(city_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Удаляет город по ID.

    - **city_id**: ID удаляемого города.

    Возвращает сообщение об успешном удалении.
    """
    city = db.query(City).filter(City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"message": "City deleted successfully"}


@city_router.put("/city/{city_id}", response_model=CityResponse)
async def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)) -> CityResponse:
    """
    Обновляет информацию о городе.

    - **city_id**: ID города для обновления.
    - **city**: Объект CityCreate с обновляемыми данными.

    Возвращает обновленный объект города.
    """
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found.")
    db_city.name = city.name  # type: ignore
    db_city.description = city.description  # type: ignore
    db_city.image_url = city.image_url  # type: ignore
    db.commit()
    db.refresh(db_city)
    return db_city


@city_router.get('/city/{city_id}/travels', response_model=list[TravelResponse])
async def get_travels_by_city(city_id: int, db: Session = Depends(get_db)) -> List[Travel]:
    """
    поиск вес travels в укащанов гораде.

    - **city_id**: ID города для обновления.

    Возвращает travels в указаном городе.
    """
    travels = db.query(Travel).filter(Travel.city_id == city_id).all()
    return travels