from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer, nullable=False)  # Manually entered
    genre = Column(String(100))
    language = Column(String(50))
    price = Column(DECIMAL(10, 2))
    rating = Column(DECIMAL(3, 2))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
