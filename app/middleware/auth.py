from datetime import datetime, timedelta
import os
from zoneinfo import ZoneInfo
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt import encode, decode, DecodeError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.models import User

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24h

INVALID_CREDENTIALS = HTTPException(
  status_code=status.HTTP_400_BAD_REQUEST,
  detail='Invalid credentials in request body',
  headers={'WWW-authenticate': 'Bearer'},
)
UNAUTHORIZED_CREDENTIALS = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user', headers={'WWW-authenticate': 'Bearer'}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  to_encode.update({'exp': expire})
  encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def check_auth_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
  try:
    payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get('sub')
    if not username:
      raise INVALID_CREDENTIALS

    stmt = select(User).where(User.username == username)
    user = db.scalar(stmt)

    if not user:
      raise UNAUTHORIZED_CREDENTIALS

    return user
  except DecodeError:
    raise DecodeError
