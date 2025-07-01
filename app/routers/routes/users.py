from app.schemas import UserSchema, UserList
from app.database.database import get_db, create_tables
from app.models import User
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(prefix='/users', tags=['users'])
auth_schema = HTTPBearer()

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
  try:
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')


# get all
@router.get('/', response_model=list[UserList])
def get_users(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(auth_schema)):
  users = db.query(User).all()
  return users


# get by id
@router.get('/{user_id}', response_model=UserList)
def get_user_id(
  user_id: int, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(auth_schema)
):
  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
  return user


# atualizar tudo
@router.put('/{user_id}', status_code=status.HTTP_200_OK)
def update_user(
  user_id: int,
  user: UserSchema,
  db: Session = Depends(get_db),
  credentials: HTTPAuthorizationCredentials = Depends(auth_schema),
):
  db_user = db.query(User).filter(User.id == user_id).first()
  if not db_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

  db_user.username = user.username
  db_user.email = user.email
  db.commit()
  db.refresh(db_user)
  return db_user


# atualizar
@router.patch('/{user_id}', status_code=status.HTTP_200_OK)
def partial_update_user(
  user_id: int,
  user: UserSchema,
  db: Session = Depends(get_db),
  credentials: HTTPAuthorizationCredentials = Depends(auth_schema),
):
  db_user = db.query(User).filter(User.id == user_id).first()
  if not db_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

  if user.username:
    db_user.username = user.username
  if user.email:
    db_user.email = user.email
  db.commit()
  db.refresh(db_user)
  return db_user