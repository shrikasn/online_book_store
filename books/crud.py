from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from books.model import Book
from books.schema import BookCreate

async def create_book(db: AsyncSession, book: BookCreate):
    new_book = Book(**book.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

async def get_books(db: AsyncSession):
    result = await db.execute(select(Book))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int):
    return await db.get(Book, book_id)

async def update_book(db: AsyncSession, book_id: int, book: BookCreate):
    existing_book = await db.get(Book, book_id)
    if existing_book:
        for key, value in book.dict(exclude_unset=True).items():
            setattr(existing_book, key, value)
        await db.commit()
        await db.refresh(existing_book)
        return existing_book
    return None

async def delete_book(db: AsyncSession, book_id: int):
    book = await db.get(Book, book_id)
    if book:
        await db.delete(book)
        await db.commit()
        return True
    return False
