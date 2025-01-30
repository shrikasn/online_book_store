from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession #SQLAlchemy, a python Object-Relational Mapping library to perform async db operations
from sqlalchemy.orm import sessionmaker # creates Sessions
from sqlalchemy.ext.declarative import declarative_base#it keeps track of all the models and tables
import os # used to connect the os
from dotenv import load_dotenv #simplifies the management of sensitive configuration details
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from feedback.schemas import FeedbackCreate, Feedback  # Import Feedback model here
from feedback import crud
load_dotenv() 
  

DATABASE_URL = os.getenv("DATABASE_URL") #configure the database connection.
#creates an async db , connects to the specific db url 
engine = create_async_engine(DATABASE_URL, echo=True) 

router = APIRouter()

SessionLocal = sessionmaker(
    #binds the engine, creates an async session, makes sure it does not expire
    bind=engine , class_=AsyncSession, expire_on_commit=False
)

def get_db():
    db = SessionLocal() #creates the local session
    try:
        yield db #gives the db session to the user
    finally:
        db.close() #makes sure the session is closed after use.


router = APIRouter()

@router.post("/", response_model=Feedback)
async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_feedback(db, feedback)

@router.get("/{feedback_id}", response_model=Feedback)
async def get_feedback(feedback_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_feedback(db, feedback_id)

@router.get("/", response_model=list[Feedback])
async def get_feedback_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_feedback_list(db, skip, limit)

@router.put("/{feedback_id}", response_model=Feedback)
async def update_feedback(feedback_id: int, feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_feedback(db, feedback_id, feedback)

@router.delete("/{feedback_id}", response_model=Feedback)
async def delete_feedback(feedback_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_feedback(db, feedback_id)
