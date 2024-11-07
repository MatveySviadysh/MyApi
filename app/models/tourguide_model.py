from models.city_model import CityResponse
from utils.classes import TourGuideBase


class TourGuideCreate(TourGuideBase):
    city_id: int

class TourGuideResponse(TourGuideBase):
    id: int
    city: CityResponse
    class Config:
        orm_mode = True