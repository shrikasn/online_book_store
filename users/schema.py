from pydantic import BaseModel
from datetime import date, datetime

class UserBase(BaseModel):
    name: str
    phone_number: str
    dob: date

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime  # Change to datetime
    updated_at: datetime  # Change to datetime

    class Config:
        from_attributes = True  
