from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    user_id: int
    book_id: int
    content: str

class FeedbackResponse(BaseModel):
    book_id: int
    feedback: list[str]
