from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.main import api_router
from dotenv import load_dotenv
from app.database.database import setup_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
  setup_db()
  yield


app = FastAPI(lifespan=lifespan)


# adicionar CORS
origins = '*'  # Alterar para dominios específicos em produção

app.include_router(api_router)
