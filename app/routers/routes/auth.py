from app.database.database import get_session
from app.middleware.auth import create_access_token
from app.models import User
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from sqlalchemy import select
from app.schemas import LoginSchema

from app.utils.hash import check_password

router = APIRouter(prefix='/auth', tags=['auth'])

INVALID_LOGIN_EXCEPTION = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED,
  detail='Incorrect user or password',
)


@router.post('/login', status_code=status.HTTP_200_OK)
def login(payload: LoginSchema, db: Session = Depends(get_session)):
  stmt = select(User).where(User.username == payload.username)
  user = db.scalar(stmt)

  if not user:
    raise INVALID_LOGIN_EXCEPTION

  if not check_password(payload.password, user.password):
    raise INVALID_LOGIN_EXCEPTION

  token = create_access_token(data={'sub': user.username})

  return {'access_token': token, 'type': 'Bearer'}
