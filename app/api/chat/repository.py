import sqlalchemy
from sqlalchemy import select

from app.core.database import models
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository:

    @staticmethod
    async def insert_chat(session: AsyncSession, title: str) -> models.Chat:
        chat = models.Chat(title=title)
        session.add(chat)
        await session.commit()
        await session.refresh(chat)
        return chat

    @staticmethod
    async def select_chat_by_id(
        session: AsyncSession, chat_id: int
    ) -> models.Chat | None:
        result = await session.execute(
            select(models.Chat).where(models.Chat.id == chat_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def delete_chat(session: AsyncSession, chat_id: int) -> None:
        await session.execute(
            sqlalchemy.delete(models.Chat).where(models.Chat.id == chat_id)
        )
        await session.commit()

    @staticmethod
    async def insert_message(
        session: AsyncSession, chat_id: int, text: str
    ) -> models.Message:
        message = models.Message(chat_id=chat_id, text=text)
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message

    @staticmethod
    async def select_last_messages(
        session: AsyncSession, chat_id: int, limit: int
    ) -> list[models.Message]:
        result = await session.execute(
            select(models.Message)
            .where(models.Message.chat_id == chat_id)
            .order_by(models.Message.created_at.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))
