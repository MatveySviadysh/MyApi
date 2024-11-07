from database.models import User
from models.travel_model import TravelResponse
from utils.classes import OrderBase


class OrderCreate(OrderBase):
    user_id: int
    travel_id: int

class OrderResponse(OrderBase):
    id: int
    user: User
    travel: TravelResponse
    class Config:
        orm_mode = True