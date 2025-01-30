from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, ForeignKey, select, exists
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel

DATABASE_URL = "mysql+aiomysql://root:Prasad%408@localhost/book_store"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()

# Dependency to get the async database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Define the Authors model
class Author(Base):
    __tablename__ = "authors"
    author_id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(255), unique=True, index=True)

# Define the Book model (now includes author_id)
class Book(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    rating = Column(Float)
    author_id = Column(Integer, ForeignKey("authors.author_id"))

# Define the Order model
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))

# Define the Feedback model
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    user_id = Column(Integer)  # Feedback given by user
    content = Column(String(500))  # Feedback content

app = FastAPI()

# Pydantic model for feedback submission
class FeedbackCreate(BaseModel):
    user_id: int
    book_id: int
    content: str

# Get book details for a user
@app.get("/user/{user_id}/orders")
async def get_user_orders(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Book.title, Book.rating)
        .join(Order, Order.book_id == Book.book_id)
        .filter(Order.user_id == user_id)
    )
    result = await db.execute(stmt)
    books = result.fetchall()
    return {"user_id": user_id, "books": [{"title": title, "rating": rating} for title, rating in books]}  

# Get all orders (order ID & book ID) for a specific user
@app.get("/user/{user_id}/orders/details")
async def get_user_orders_details(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Order.id, Order.book_id).filter(Order.user_id == user_id)
    result = await db.execute(stmt)
    orders = result.fetchall()
    return {"user_id": user_id, "orders": [{"order_id": order_id, "book_id": book_id} for order_id, book_id in orders]}

# Get all feedback for a specific book
@app.get("/book/{book_id}/feedback")
async def get_book_feedback(book_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Feedback.content).filter(Feedback.book_id == book_id)
    result = await db.execute(stmt)
    feedback_list = result.fetchall()
    return {"book_id": book_id, "feedback": [content for (content,) in feedback_list]}

# Allow feedback only for purchased books
@app.post("/feedback/add")
async def add_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    # Check if user has ordered the book
    order_check = await db.execute(
        select(exists().where(Order.user_id == feedback.user_id, Order.book_id == feedback.book_id))
    )
    order_exists = order_check.scalar()

    if not order_exists:
        raise HTTPException(status_code=403, detail="User has not ordered this book. Feedback not allowed.")

    # Add feedback to the database
    new_feedback = Feedback(user_id=feedback.user_id, book_id=feedback.book_id, content=feedback.content)
    db.add(new_feedback)
    await db.commit()
    return {"message": "Feedback added successfully"}

@app.get("/books")
async def get_books(page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    stmt = select(Book.title, Book.rating).offset((page - 1) * limit).limit(limit)
    result = await db.execute(stmt)
    books = result.fetchall()
    
    return {"page": page, "limit": limit, "books": [{"title": title, "rating": rating} for title, rating in books]}
