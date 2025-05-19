from app.schemas import UserSchema
from app.database.database import get_db, create_tables
from app.models import User
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(prefix='/users', tags=['users'])


# Criar tabelas ao iniciar a aplicação
create_tables()


# Cria um novo usuário
@router.post('/')
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
