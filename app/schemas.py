from pydantic import BaseModel


class UserSchema(BaseModel):
  username: str
  email: str
  password: str


class UserUpdateSchema(BaseModel):
  username: str | None = None
  email: str | None = None


class UserList(BaseModel):
  id: int
  username: str
  email: str
