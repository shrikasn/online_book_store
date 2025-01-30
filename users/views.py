from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from users.model import User
from users.schema import UserCreate, UserResponse
from users.crud import create_user, get_user_by_id, update_user, delete_user
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession #SQLAlchemy, a python Object-Relational Mapping library to perform async db operations
from sqlalchemy.orm import sessionmaker # creates Sessions
from sqlalchemy.ext.declarative import declarative_base#it keeps track of all the models and tables
import os # used to connect the os
from dotenv import load_dotenv #simplifies the management of sensitive configuration details
from sqlalchemy.orm import Session

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


@router.post("/", response_model=UserResponse)
async def create_user_view(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user_view(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_view(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await update_user(db, user_id, user)

@router.delete("/{user_id}")
async def delete_user_view(user_id: int, db: AsyncSession = Depends(get_db)):
    await delete_user(db, user_id)
    return {"detail": "User deleted successfully"}
