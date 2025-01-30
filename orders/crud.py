from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from orders.model import Order
from orders.schema import OrderCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

# Create order
async def create_order(db: AsyncSession, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    try:
        await db.commit()
        await db.refresh(db_order)
        return db_order
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity error while creating order"
        )

# Get all orders
async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Order).offset(skip).limit(limit))
    orders = result.scalars().all()
    return orders

# Get a single order by ID
async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order

# Update order
async def update_order(db: AsyncSession, order_id: int, order: OrderCreate):
    db_order = await get_order(db, order_id)
    for key, value in order.dict().items():
        setattr(db_order, key, value)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

# Delete order
async def delete_order(db: AsyncSession, order_id: int):
    db_order = await get_order(db, order_id)
    await db.delete(db_order)
    await db.commit()
    return {"message": "Order deleted successfully"}
