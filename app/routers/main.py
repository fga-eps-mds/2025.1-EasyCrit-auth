from fastapi import APIRouter
from app.routers.routes import users
from app.routers.routes import auth

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(auth.auth_router)