from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers.main import api_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# adicionar CORS
origins = "*"  # Alterar para dominios específicos em produção

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
