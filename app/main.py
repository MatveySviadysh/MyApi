from fastapi import FastAPI
from routes.user import user_router
from routes.city import city_router

app = FastAPI()

app.include_router(user_router)
app.include_router(city_router)