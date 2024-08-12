from sqlalchemy import Column, Integer, String, ForeignKey, UUID, JSON, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    logins = relationship('Logins', back_populates='account')

    def __repr__(self):
        return f'<Account {self.email}>'
    
class Logins(Base):
    __tablename__ = 'logins'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    created_at = Column(DateTime(timezone=True), default=func.now())
    ip_address = Column(String, nullable=False)
    is_suspicious = Column(Boolean, default=False)
    
    account = relationship('Account', back_populates='logins')
    
    def __repr__(self):
        return f'<Login {self.login_time}>'
    
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(UUID, nullable=False)
    message = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
