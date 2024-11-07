from fastapi import FastAPI
from app.routes.items import post_router
from app.routes.user import user_router

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)
