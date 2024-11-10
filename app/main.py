from fastapi import FastAPI
from routes.user import user_router
from routes.city import city_router
from routes.travel import travel_router
from routes.tour_guide import tour_guide_router
app = FastAPI()

app.include_router(user_router)
app.include_router(city_router)
app.include_router(tour_guide_router)
app.include_router(travel_router)