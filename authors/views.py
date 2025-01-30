from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from authors import crud, schema  # Corrected to 'schemas' from 'schema'
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection configuration
DATABASE_URL = os.getenv("DATABASE_URL")  # Ensure the environment variable is correctly set
engine = create_async_engine(DATABASE_URL, echo=True)

# Session creation using AsyncSession
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the FastAPI router
router = APIRouter()

# POST: Create a new author
@router.post("/authors/", response_model=schema.Author)
async def create_author(author: schema.AuthorCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_author(db, author)

# GET: Read a specific author by author_id
@router.get("/authors/{author_id}", response_model=schema.Author)
async def read_author(author_id: int, db: AsyncSession = Depends(get_db)):
    db_author = await crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

# GET: Read multiple authors with pagination (skip and limit)
#@router.get("/authors/", response_model=list[schema.Author])
#async def read_authors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    #authors = await crud.get_authors(db, skip, limit)
    #return authors

# PUT: Update an existing author by author_id
@router.put("/authors/{author_id}", response_model=schema.Author)
async def update_author(author_id: int, author: schema.AuthorCreate, db: AsyncSession = Depends(get_db)):
    db_author = await crud.update_author(db, author_id, author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

# DELETE: Delete an author by author_id
@router.delete("/authors/{author_id}", response_model=schema.Author)
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    db_author = await crud.delete_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author
