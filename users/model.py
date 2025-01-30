from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15), nullable=False)
    dob = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
