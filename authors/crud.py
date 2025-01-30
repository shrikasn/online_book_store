from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from authors.model import Author
from authors.schema import AuthorCreate

async def create_author(db: AsyncSession, author: AuthorCreate):
    db_author = Author(name=author.name, nationality=author.nationality, dob=author.dob, no_of_books=author.no_of_books)
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author

async def get_author(db: AsyncSession, author_id: int):
    result = await db.execute(select(Author).filter(Author.author_id == author_id))
    return result.scalars().first()

async def get_authors(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Author).offset(skip).limit(limit))
    return result.scalars().all()

async def update_author(db: AsyncSession, author_id: int, author: AuthorCreate):
    db_author = await get_author(db, author_id)
    if db_author:
        db_author.name = author.name
        db_author.nationality = author.nationality
        db_author.dob = author.dob
        db_author.no_of_books = author.no_of_books
        await db.commit()
        await db.refresh(db_author)
        return db_author
    return None

async def delete_author(db: AsyncSession, author_id: int):
    db_author = await get_author(db, author_id)
    if db_author:
        await db.delete(db_author)
        await db.commit()
        return db_author
    return None
