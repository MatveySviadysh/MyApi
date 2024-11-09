from datetime import date
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    age: int


class TravelBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    duration: str
    start_date: date
    end_date: date
    image_url: Optional[str] = None


class TourGuideBase(BaseModel):
    name: str
    experience_years: int
    bio: Optional[str] = None
    contact_info: str


class CityBase(BaseModel):
    name: str
    description: str
    image_url: Optional[str] = None


class OrderBase(BaseModel):
    order_date: date
    status: str


class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    created_at: date