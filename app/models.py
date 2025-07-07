from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database.database import Base


class UserRoles(Enum):
  DUNGEON_MASTER = 'dungeon master'
  PLAYER = 'player'


class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String)
  role = Column(SQLAlchemyEnum(UserRoles), nullable=False, default=UserRoles.PLAYER)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  characters = relationship('Character', back_populates='user', cascade='all, delete-orphan')

  sessions = relationship('Session', back_populates='user', cascade='all, delete-orphan')


class Character(Base):
  __tablename__ = 'characters'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  biography = Column(String)
  circle_color = Column(String)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  user = relationship('User', back_populates='characters')


class Sessions(Base):
  __tablename__ = 'sessions'

  id = Column(Integer, primary_key=True, index=True)
  dungeon_master_id = Column(Integer, ForeignKey('users.id'), nullable=False)

  dungeon_master = relationship('User', back_populates='sessions')


class PlayersSessions(Base):
  __tablename__ = 'players_sessions'

  player_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
  sessions_id = Column(Integer, ForeignKey('sessions.id'), primary_key=True, nullable=False)
