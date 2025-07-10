from pydantic import BaseModel
from app.models import UserRoles


class LoginSchema(BaseModel):
  username: str
  password: str


# User
# Base for all other user schemas
class UserBase(BaseModel):
  username: str
  email: str


class UserPublic(UserBase):
  id: int
  role: UserRoles


class UserCreate(UserBase):
  password: str
  role: UserRoles


class UserUpdate(BaseModel):
  username: str | None = None
  email: str | None = None
  password: str | None = None


class UserList(BaseModel):
  users: list[UserPublic]


# TODO: Characters
class CharacterBase(BaseModel):
  name: str
  biography: str
  circle_color: str
  user_id: str
