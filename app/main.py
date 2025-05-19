from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas import UserSchema
from app.models import User
from app.database.database import get_db, create_tables

app = FastAPI()

# adicionar CORS
origins = '*'  # Alterar para dominios específicos em produção

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

# Criar tabelas ao iniciar a aplicação
create_tables()

@app.get('/')
def read_root():
  return {'message': 'Bem vindo à API de autenticação!'}

# Cria um novo usuário
@app.post('/users') 
def create_user(user: UserSchema, db: Session = Depends(get_db)):
  db_user = User(
    username=user.username,
    email=user.email,
    password=user.password,
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


