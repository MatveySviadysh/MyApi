from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import TourGuide, City
from models.tourguide_model import TourGuideCreate, TourGuideResponse
from utils.helpers import get_db
from sqlalchemy.orm import joinedload

tour_guide_router = APIRouter()


@tour_guide_router.post('/tour_guide/create', response_model=TourGuideResponse)
async def create_tour_guide(tour_guide: TourGuideCreate, db: Session = Depends(get_db)) ->TourGuide:
    existing_tour_guide = db.query(TourGuide).filter(TourGuide.name == tour_guide.name).first()
    if existing_tour_guide:
        raise HTTPException(status_code=400, detail="Tour guide with this name already exists.")
    city = db.query(City).filter(City.id == tour_guide.city_id).first()
    if not city:
        raise HTTPException(status_code=400, detail="City not found.")
    
    db_tour_guide = TourGuide(
        name=tour_guide.name,
        experience_years=tour_guide.experience_years,
        bio=tour_guide.bio,
        contact_info=tour_guide.contact_info,
        city_id=tour_guide.city_id 
    )
    db.add(db_tour_guide)
    db.commit()
    db.refresh(db_tour_guide)
    return db_tour_guide


@tour_guide_router.get('/tour_guides/', response_model=List[TourGuideResponse])
def read_tour_guides(db: Session = Depends(get_db)) -> List[TourGuide]:
    return db.query(TourGuide).options(joinedload(TourGuide.city)).all()


@tour_guide_router.get('/tour_guide/{id}', response_model=TourGuideResponse)
async def search_tour_guide(id: int, db: Session = Depends(get_db)):
    tour_guide = db.query(TourGuide).filter(TourGuide.id == id).first()
    if not tour_guide:
        raise HTTPException(status_code=404, detail="Tour guide not found")
    return tour_guide


@tour_guide_router.delete('/tour_guide/{id}')
async def delete_tour_guide(id: int, db: Session = Depends(get_db)):
    tour_guide = db.query(TourGuide).filter(TourGuide.id == id).first()
    if not tour_guide:
        raise HTTPException(status_code=404, detail="Tour guide not found")
    db.delete(tour_guide)
    db.commit()
    return {"message": "tour_guide deleted successfully"}


@tour_guide_router.put('/tour_guide/{id}', response_model=TourGuideResponse)
async def update_tour_guide(id: int, tour_guide: TourGuideCreate, db: Session = Depends(get_db)):
    db_tour_guide = db.query(TourGuide).filter(TourGuide.id == id).first()
    if not db_tour_guide:
        raise HTTPException(status_code=404, detail="Tour guide not found")
    db_tour_guide.name = tour_guide.name # type: ignore
    db_tour_guide.experience_years = tour_guide.experience_years # type: ignore
    db_tour_guide.bio = tour_guide.bio # type: ignore
    db_tour_guide.contact_info = tour_guide.contact_info # type: ignore
    db.commit()
    db.refresh(db_tour_guide)
    return db_tour_guide