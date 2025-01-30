from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    
    author_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    nationality = Column(String(100))
    dob = Column(Date)
    no_of_books = Column(Integer)
