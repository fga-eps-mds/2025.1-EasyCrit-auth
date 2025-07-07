from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.main import api_router
from dotenv import load_dotenv
from app.middleware.auth import JWTAuthMiddleware
from app.database.database import setup_db

load_dotenv()

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
  setup_db()
  yield


# adicionar CORS
origins = '*'  # Alterar para dominios específicos em produção

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.add_middleware(JWTAuthMiddleware)

app.include_router(api_router)
