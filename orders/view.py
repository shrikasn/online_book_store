from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from orders.schema import OrderCreate, Order
from orders.crud import create_order, get_orders, get_order, update_order, delete_order
#from app.model import SessionLocal
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



# Create order
@router.post("/orders/", response_model=Order)
async def create_order_view(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await create_order(db=db, order=order)

# Get all orders
@router.get("/orders/", response_model=list[Order])
async def get_orders_view(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_orders(db=db, skip=skip, limit=limit)

# Get a single order by ID
@router.get("/orders/{order_id}", response_model=Order)
async def get_order_view(order_id: int, db: AsyncSession = Depends(get_db)):
    return await get_order(db=db, order_id=order_id)

# Update order
@router.put("/orders/{order_id}", response_model=Order)
async def update_order_view(order_id: int, order: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await update_order(db=db, order_id=order_id, order=order)

# Delete order
@router.delete("/orders/{order_id}")
async def delete_order_view(order_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_order(db=db, order_id=order_id)
