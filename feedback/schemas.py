from pydantic import BaseModel
from datetime import datetime

class FeedbackBase(BaseModel):
    user_id: int
    book_id: int
    content: str

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    created_at: datetime
    updated_at: datetime


    class Config:
         from_attributes = True  
