from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.chat import schemas
from app.api.chat.repository import ChatRepository


class ChatService:

    @staticmethod
    async def create_chat(
        session: AsyncSession, data: schemas.ChatCreateRequest
    ) -> schemas.CreateChatResponse:
        title = data.title.strip()

        if not title:
            raise HTTPException(status_code=422, detail="Title cannot be empty")

        chat = await ChatRepository.insert_chat(session=session, title=title)

        return schemas.CreateChatResponse.model_validate(chat)

    @staticmethod
    async def send_message(
        session: AsyncSession, chat_id: int, data: schemas.SendMessageRequest
    ) -> schemas.SendMessageResponse:
        chat = await ChatRepository.select_chat_by_id(session=session, chat_id=chat_id)

        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        message = await ChatRepository.insert_message(session=session, chat_id=chat_id, text=data.text)

        return schemas.SendMessageResponse.model_validate(message)

    @staticmethod
    async def get_chat_with_messages(
        session: AsyncSession, chat_id: int, limit: int
    ) -> schemas.ChatWithMessagesResponse:
        chat = await ChatRepository.select_chat_by_id(session=session, chat_id=chat_id)

        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        messages = await ChatRepository.select_last_messages(
            session=session, 
            chat_id=chat_id, 
            limit=limit
        )

        messages_out = [
            schemas.SendMessageResponse.model_validate(msg) for msg in messages
        ]

        return schemas.ChatWithMessagesResponse(
            id=chat.id,
            title=chat.title,
            created_at=chat.created_at,
            messages=messages_out,
        )

    @staticmethod
    async def delete_chat(
        session: AsyncSession, chat_id: int
    ) -> schemas.DeleteChatResponse:
        chat = await ChatRepository.select_chat_by_id(session=session, chat_id=chat_id)

        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        await ChatRepository.delete_chat(session=session, chat_id=chat_id)

        return schemas.DeleteChatResponse(success=True)
