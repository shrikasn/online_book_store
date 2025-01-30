from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

# Base class
Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    author_id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(255), unique=True, index=True)

class Book(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    rating = Column(Float)
    author_id = Column(Integer, ForeignKey("authors.author_id"))

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    user_id = Column(Integer)
    content = Column(String(500))
