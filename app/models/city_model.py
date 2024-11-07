from utils.classes import CityBase


class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: int
    class Config:
        orm_mode = True