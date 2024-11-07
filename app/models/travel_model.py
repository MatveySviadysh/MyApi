from typing import Optional
from models.city_model import CityResponse
from models.tourguide_model import TourGuideResponse
from utils.classes import TravelBase


class TravelCreate(TravelBase):
    city_id: int
    guide_id: Optional[int] = None

class TravelResponse(TravelBase):
    id: int
    city: CityResponse
    guide: TourGuideResponse
    class Config:
        orm_mode = True