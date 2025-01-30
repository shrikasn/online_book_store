from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy import exists
from api.models import Book, Order, Feedback

async def get_user_books(user_id: int, db: Session):
    stmt = (
        select(Book.title, Book.rating)
        .join(Order, Order.book_id == Book.book_id)
        .filter(Order.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.fetchall()

async def get_user_orders(user_id: int, db: Session):
    stmt = select(Order.id, Order.book_id).filter(Order.user_id == user_id)
    result = await db.execute(stmt)
    return result.fetchall()

async def get_book_feedback(book_id: int, db: Session):
    stmt = select(Feedback.content).filter(Feedback.book_id == book_id)
    result = await db.execute(stmt)
    return result.fetchall()

async def check_user_ordered_book(user_id: int, book_id: int, db: Session):
    stmt = select(exists().where(Order.user_id == user_id, Order.book_id == book_id))
    result = await db.execute(stmt)
    return result.scalar()

async def add_feedback_to_db(feedback, db: Session):
    new_feedback = Feedback(user_id=feedback.user_id, book_id=feedback.book_id, content=feedback.content)
    db.add(new_feedback)
    await db.commit()
