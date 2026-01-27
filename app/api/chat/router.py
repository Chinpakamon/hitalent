from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.chat import exceptions, schemas, service
from app.core.database.core import get_session

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/", response_model=schemas.CreateChatResponse)
@exceptions.handle_errors(
    [
        (ValueError, 422, "Validation error: {e}"),
    ]
)
async def create_chat(
    data: schemas.ChatCreateRequest, session: AsyncSession = Depends(get_session)
):
    return await service.ChatService.create_chat(session=session, data=data)


@router.post("/{chat_id}/messages/", response_model=schemas.SendMessageResponse)
@exceptions.handle_errors(
    [
        (ValueError, 422, "Validation error: {e}"),
    ]
)
async def send_message(
    chat_id: int,
    data: schemas.SendMessageRequest,
    session: AsyncSession = Depends(get_session),
):
    return await service.ChatService.send_message(session=session, chat_id=chat_id, data=data)


@router.get("/{chat_id}", response_model=schemas.ChatWithMessagesResponse)
@exceptions.handle_errors(
    [
        (ValueError, 422, "Validation error: {e}"),
    ]
)
async def get_chat(
    chat_id: int,
    limit: int = Query(20, gt=0, le=100),
    session: AsyncSession = Depends(get_session),
):
    return await service.ChatService.get_chat_with_messages(session=session, chat_id=chat_id, limit=limit)


@router.delete("/{chat_id}", response_model=schemas.DeleteChatResponse)
@exceptions.handle_errors(
    [
        (ValueError, 422, "Validation error: {e}"),
    ]
)
async def delete_chat(chat_id: int, session: AsyncSession = Depends(get_session)):
    await service.ChatService.delete_chat(session=session, chat_id=chat_id)
    return schemas.DeleteChatResponse(success=True)
