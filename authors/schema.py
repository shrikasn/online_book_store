from pydantic import BaseModel
from datetime import date
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    nationality: Optional[str] = None
    dob: Optional[date] = None
    no_of_books: Optional[int] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    author_id: int

    class Config:
         from_attributes = True  
