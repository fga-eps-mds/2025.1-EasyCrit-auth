from app.schemas import UserCreate, UserList, UserUpdate, UserPublic
from app.database.database import get_session
from app.models import User
from app.middleware.auth import check_auth_token
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils.hash import hash_password

router = APIRouter(prefix='/users', tags=['users'])
auth_schema = HTTPBearer()


# Cria um novo usuário
@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
  stmt = select(User).where((User.username == user.username) | (User.email == user.email))
  db_user = db.scalar(stmt)

  if db_user and db_user.username == user.username:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='A user with that username already exists on databse.'
    )

  if db_user and db_user.email == user.email:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, detail='A user with that email already exists on databse.'
    )

  db_user = User(username=user.username, email=user.email, password=hash_password(user.password), role=user.role)

  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


# get all
@router.get('/', response_model=UserList, dependencies=[Depends(check_auth_token)])
def get_users(
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(get_session),
):
  try:
    stmt = select(User).offset(skip).limit(limit).order_by(User.id)
    res = db.scalars(stmt).all()
    return {'users': res}
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


# get by id
@router.get(
  '/{user_id}', response_model=UserPublic, dependencies=[Depends(check_auth_token)], status_code=status.HTTP_200_OK
)
def get_user_id(user_id: int, db: Session = Depends(get_session)):
  stmt = select(User).where(User.id == user_id)
  user = db.scalar(stmt)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
  return user


# atualizar tudo
@router.put(
  '/{user_id}', response_model=UserPublic, dependencies=[Depends(check_auth_token)], status_code=status.HTTP_200_OK
)
def update_user(
  user_id: int,
  user: UserUpdate,
  db: Session = Depends(get_session),
  credentials: HTTPAuthorizationCredentials = Depends(auth_schema),
):
  stmt = select(User).where(User.id == user_id)
  db_user = db.scalar(stmt)
  if not db_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

  db_user.username = user.username
  db_user.email = user.email
  db.commit()
  db.refresh(db_user)
  return db_user


# atualizar
@router.patch(
  '/{user_id}', response_model=UserPublic, dependencies=[Depends(check_auth_token)], status_code=status.HTTP_200_OK
)
def partial_update_user(
  user_id: int,
  user: UserUpdate,
  db: Session = Depends(get_session),
):
  stmt = select(User).where(User.id == user_id)
  db_user = db.scalar(stmt)
  if not db_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

  if user.username:
    db_user.username = user.username
  if user.email:
    db_user.email = user.email
  if user.password:
    db_user.password = user.password
  db.commit()
  db.refresh(db_user)
  return db_user


@router.delete('/{user_id}', dependencies=[Depends(check_auth_token)], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_session)):
  stmt = select(User).where(User.id == user_id)
  db_user = db.scalar(stmt)

  if not db_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

  db.delete(db_user)
  db.commit()

  return {'message': 'User deleted successfully'}
