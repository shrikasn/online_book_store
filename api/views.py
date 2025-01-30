# app/views.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.models import Book, Feedback
from api.crud import get_user_books, get_user_orders, get_book_feedback, check_user_ordered_book, add_feedback_to_db
from api.schemas import FeedbackCreate
#from api.dependencies import get_db  # Dependency for getting DB session
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




import os
from dotenv import load_dotenv

load_dotenv()

# Load database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Create the AsyncSession engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create APIRouter instance for handling routes
router = APIRouter()

@router.get("/user/{user_id}/orders")
async def get_user_orders_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get the list of books ordered by a specific user.
    """
    books = await get_user_books(user_id, db)
    return {"user_id": user_id, "books": [{"title": title, "rating": rating} for title, rating in books]}

@router.get("/user/{user_id}/orders/details")
async def get_user_orders_details(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get detailed information (order ID and book ID) about a user's orders.
    """
    orders = await get_user_orders(user_id, db)
    return {"user_id": user_id, "orders": [{"order_id": order_id, "book_id": book_id} for order_id, book_id in orders]}

@router.get("/book/{book_id}/feedback")
async def get_book_feedback_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get feedback for a specific book.
    """
    feedback_list = await get_book_feedback(book_id, db)
    return {"book_id": book_id, "feedback": [content for (content,) in feedback_list]}

@router.post("/feedback/add")
async def add_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    """
    Add feedback for a book, ensuring the user has ordered the book.
    """
    order_exists = await check_user_ordered_book(feedback.user_id, feedback.book_id, db)
    if not order_exists:
        raise HTTPException(status_code=403, detail="User has not ordered this book. Feedback not allowed.")
    
    await add_feedback_to_db(feedback, db)
    return {"message": "Feedback added successfully"}

@router.get("/books")
async def get_books(page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    """
    Get a paginated list of books.
    """
    stmt = select(Book.title, Book.rating).offset((page - 1) * limit).limit(limit)
    result = await db.execute(stmt)
    books = result.fetchall()
    
    return {"page": page, "limit": limit, "books": [{"title": title, "rating": rating} for title, rating in books]}
