from sqlalchemy import Column, Integer, String, ForeignKey, Table, UUID, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)
    description = Column(String, index=True)
    
# For storing agent chat_history
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(UUID, nullable=False)
    message = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
