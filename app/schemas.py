from pydantic import BaseModel
from app.models import UserRoles


class LoginSchema(BaseModel):
  username: str
  password: str


# User
# Base for all other user schemas
class UserBase(BaseModel):
  username: str
  password: str


class UserCreate(UserBase):
  email: str
  role: UserRoles


class UserUpdateSchema(UserBase):
  email: str


class UserList(UserBase):
  id: int
  email: str
  role: UserRoles


# TODO: Characters
class CharacterBase(BaseModel):
  name: str
  biography: str
  circle_color: str
  user_id: str
