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


# Character


class CharacterBase(BaseModel):
  name: str
  biography: str
  circle_color: str


class CharacterCreate(CharacterBase):
  pass


class CharacterUpdate(BaseModel):
  name: str | None = None
  biography: str | None = None
  circle_color: str | None = None


class CharacterPublic(CharacterBase):
  id: int
  user_id: int


class CharacterList(BaseModel):
  characters: list[CharacterPublic]
