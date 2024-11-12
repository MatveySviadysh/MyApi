from database.models import User
from models.travel_model import TravelResponse
from models.user_model import UserResponse
from utils.classes import ReviewBase


class ReviewCreate(ReviewBase):
    user_id: int
    travel_id: int

class ReviewResponse(ReviewBase):
    id: int
    user: UserResponse
    travel: TravelResponse
    class Config:
        arbitrary_types_allowed = True 
        orm_mode = True