from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Base class
Base = declarative_base()

# Create an Enum for the status
class StatusEnum(str, enum.Enum):
    ordered = "ordered"
    shipped = "shipped"
    delivered = "delivered"

# Orders Model
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    ordered_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, nullable=True)
