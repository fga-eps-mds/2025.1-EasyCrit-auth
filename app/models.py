from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database.database import Base

SCHEMA_NAME = 'main'


class UserRoles(Enum):
  DUNGEON_MASTER = 'dungeon master'
  PLAYER = 'player'


class User(Base):
  __tablename__ = 'users'
  __table_args__ = {'schema': SCHEMA_NAME}

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String)
  role = Column(SQLAlchemyEnum(UserRoles), nullable=False, default=UserRoles.PLAYER)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  characters = relationship('Character', back_populates='user', cascade='all, delete-orphan')
  sessions = relationship('Session', cascade='all, delete-orphan')


class Character(Base):
  __tablename__ = 'characters'
  __table_args__ = {'schema': SCHEMA_NAME}

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.users.id'), nullable=False)
  name = Column(String)
  biography = Column(String)
  circle_color = Column(String)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  user = relationship('User', back_populates='characters')


class Session(Base):
  __tablename__ = 'sessions'
  __table_args__ = {'schema': SCHEMA_NAME}

  id = Column(Integer, primary_key=True, index=True)
  dungeon_master_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.users.id'), nullable=False)

  dungeon_master = relationship('User', back_populates='sessions')


class PlayerSession(Base):
  __tablename__ = 'players_sessions'
  __table_args__ = {'schema': SCHEMA_NAME}

  player_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.users.id'), primary_key=True, nullable=False)
  sessions_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.sessions.id'), primary_key=True, nullable=False)
