from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession #SQLAlchemy, a python Object-Relational Mapping library to perform async db operations
from sqlalchemy.orm import sessionmaker # creates Sessions
from sqlalchemy.ext.declarative import declarative_base#it keeps track of all the models and tables
import os # used to connect the os
from dotenv import load_dotenv #simplifies the management of sensitive configuration details
from sqlalchemy.orm import Session
from books.schema import BookCreate, BookResponse
from books.crud import create_book, get_books, get_book, update_book, delete_book

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
        db.close() #makes sure the session is closed after use

router = APIRouter()

@router.post("/books/", response_model=BookResponse)
async def create_new_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await create_book(db, book)

@router.get("/books/", response_model=list[BookResponse])
async def list_books(db: AsyncSession = Depends(get_db)):
    return await get_books(db)

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_single_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=BookResponse)
async def update_existing_book(book_id: int, book: BookCreate, db: AsyncSession = Depends(get_db)):
    updated_book = await update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/books/{book_id}")
async def remove_book(book_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
