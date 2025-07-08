from pydantic import BaseModel


class UserCreate(BaseModel):
  username: str
  email: str
  password: str
  role: str


class User(BaseModel):
  id: int
  username: str
  email: str
  role: str

  class Config:
    orm_mode = True


class UserUpdateSchema(BaseModel):
  username: str | None = None
  email: str | None = None
  role: str | None = None

  class Config:
    orm_mode = True


class UserList(BaseModel):
  id: int
  username: str
  email: str
  role: str

  class Config:
    orm_mode = True
