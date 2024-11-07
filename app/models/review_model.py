from database.models import User
from models.travel_model import TravelResponse
from utils.classes import ReviewBase


class ReviewCreate(ReviewBase):
    user_id: int
    travel_id: int

class ReviewResponse(ReviewBase):
    id: int
    user: User
    travel: TravelResponse
    class Config:
        orm_mode = True