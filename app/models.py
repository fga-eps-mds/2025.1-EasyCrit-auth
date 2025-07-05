from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy import Enum as SQLAlchemyEnum
from app.database.database import Base


class UserRoles(Enum):
  DUNGEON_MASTER = "dungeon master"
  PLAYER = "player"

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String)
  role = Column(
    SQLAlchemyEnum(UserRoles),
    nullalble=False,
    default=UserRoles.PLAYER
  )
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Character(Base):
  __tablename__ = 'characters'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  biography = Column(String)
  circle_color = Column(String)
  user_id = Column(Integer)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
