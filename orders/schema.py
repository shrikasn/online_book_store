from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    ordered = "ordered"
    shipped = "shipped"
    delivered = "delivered"

class OrderBase(BaseModel):
    user_id: int
    book_id: int
    status: StatusEnum
    ordered_at: datetime = None
    updated_at: datetime = None

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True
