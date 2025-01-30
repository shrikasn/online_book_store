from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author_id: int
    genre: Optional[str] = None
    language: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    book_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 
