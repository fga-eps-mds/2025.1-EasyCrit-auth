from fastapi import APIRouter
from app.routers.routes import users

api_router = APIRouter()
api_router.include_router(users.router)
