from sqlalchemy import Column, Integer, String
from app.database.database import Base


class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String)
  role = Column(String, default='player')

  def __repr__(self):
    return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}')>"
