from app.schemas import UserCreate, User, UserList
from app.database.database import get_db, create_tables
from app.models import User as UserModel 
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


router = APIRouter(prefix='/users', tags=['users'])


# Criar tabelas ao iniciar a aplicação
create_tables()


# Cria um novo usuário
@router.post('/', response_model=User) 
def create_user(user: UserCreate, db: Session = Depends(get_db)): 
  existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
  if existing_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

  hashed_password = get_password_hash(user.password)

  db_user = UserModel( 
    username=user.username,
    email=user.email,
    password=hashed_password, 
    role=user.role
  )
  try:
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Integrity error creating user')
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An error occurred: {e}')


# get all
@router.get('/', response_model=list[UserList]) 
def get_users(db: Session = Depends(get_db)):
  users = db.query(UserModel).all() 
  return users


# get by id
@router.get('/{user_id}', response_model=User) 
def get_user_id(user_id: int, db: Session = Depends(get_db)):
  user = db.query(UserModel).filter(UserModel.id == user_id).first() 
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
  return user


# atualizar tudo
@router.put('/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
  db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
  if not db_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

  db_user.username = user.username
  db_user.email = user.email
  db_user.role = user.role

  db.commit()
  db.refresh(db_user)
  return db_user


@router.patch('/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
def partial_update_user(user_id: int, user: UserUpdateSchema, db: Session = Depends(get_db)):
  db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
  if not db_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


  if user.username is not None:
    db_user.username = user.username
  if user.email is not None:
    db_user.email = user.email
  if user.role is not None: 
    db_user.role = user.role

  db.commit()
  db.refresh(db_user)
  return db_user
