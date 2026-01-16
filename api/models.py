from sqlalchemy import Column, Integer, String, DateTime, func
from api.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=False)
    password_hash = Column(String, nullable=False)
    createdate = Column(DateTime(timezone=True), server_default=func.now())
    
class eta_predictions(Base):
    __tablename__ = 'eta_predictions'

    id = Column(Integer, primary_key=True, index=True)
    prediction = Column(float, unique=True, index=True,nullable=False)    
    model_version = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


