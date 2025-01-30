from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from users.model import User
from users.schema import UserCreate

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Create a new user."""
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    """Retrieve a user by their ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def update_user(db: AsyncSession, user_id: int, user_data: UserCreate) -> User:
    """Update an existing user's details."""
    db_user = await get_user_by_id(db, user_id)
    for key, value in user_data.dict().items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int) -> None:
    """Delete a user by their ID."""
    db_user = await get_user_by_id(db, user_id)
    await db.delete(db_user)
    await db.commit()
