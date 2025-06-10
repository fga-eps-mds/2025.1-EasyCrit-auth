from app.database.database import get_db, create_tables
from app.models import User
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, UTC
import os
from app.schemas import LoginSchema


auth_router = APIRouter(prefix='/auth', tags=['auth'])

create_tables()


SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


@auth_router.post('/login')
def login(payload: LoginSchema, db: Session = Depends(get_db)):
  username = payload.username
  password = payload.password
  # username = payload.get('username')
  # password = payload.get('password')
  if not username or not password:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username and password required')

  user = db.query(User).filter(User.username == username).first()
  if not user or user.password != password:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

  to_encode = {
    'username': user.username,
    'email': user.email,
    'exp': datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
  }
  token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return {'access_token': token, 'token_type': 'bearer'}
