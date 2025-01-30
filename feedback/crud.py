from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from feedback.model import Feedback as FeedbackModel
from feedback.schemas import FeedbackCreate, Feedback

async def create_feedback(db: AsyncSession, feedback: FeedbackCreate) -> Feedback:
    db_feedback = FeedbackModel(
        user_id=feedback.user_id,
        book_id=feedback.book_id,
        content=feedback.content,
    )
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

async def get_feedback(db: AsyncSession, feedback_id: int) -> Feedback:
    stmt = select(FeedbackModel).filter(FeedbackModel.id == feedback_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_feedback_list(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Feedback]:
    stmt = select(FeedbackModel).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_feedback(db: AsyncSession, feedback_id: int, feedback: FeedbackCreate) -> Feedback:
    stmt = select(FeedbackModel).filter(FeedbackModel.id == feedback_id)
    result = await db.execute(stmt)
    db_feedback = result.scalars().first()
    if db_feedback:
        db_feedback.user_id = feedback.user_id
        db_feedback.book_id = feedback.book_id
        db_feedback.content = feedback.content
        await db.commit()
        await db.refresh(db_feedback)
    return db_feedback

async def delete_feedback(db: AsyncSession, feedback_id: int) -> Feedback:
    stmt = select(FeedbackModel).filter(FeedbackModel.id == feedback_id)
    result = await db.execute(stmt)
    db_feedback = result.scalars().first()
    if db_feedback:
        await db.delete(db_feedback)
        await db.commit()
    return db_feedback
