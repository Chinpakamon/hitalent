from datetime import datetime

import pydantic


class ChatCreateRequest(pydantic.BaseModel):
    """Запрос на создание чата"""

    title: str = pydantic.Field(..., min_length=1, max_length=200)

    @classmethod
    def validate_title(cls, v: str) -> str:
        return v.strip()


class CreateChatResponse(pydantic.BaseModel):
    """Ответ при создании чата"""

    id: int
    title: str
    created_at: datetime

    model_config = pydantic.ConfigDict(from_attributes=True)



class SendMessageRequest(pydantic.BaseModel):
    """Запрос на отправку сообщения"""

    text: str = pydantic.Field(..., min_length=1, max_length=5000)

    @classmethod
    def validate_text(cls, v: str) -> str:
        return v.strip()


class SendMessageResponse(pydantic.BaseModel):
    """Ответ при создании сообщения"""

    id: int
    chat_id: int
    text: str
    created_at: datetime

    model_config = pydantic.ConfigDict(from_attributes=True)


class ChatWithMessagesResponse(pydantic.BaseModel):
    """Ответ для GET /chats/{chat_id} с последними сообщениями"""

    id: int
    title: str
    created_at: datetime
    messages: list[SendMessageResponse]

    model_config = pydantic.ConfigDict(from_attributes=True)


class DeleteChatRequest(pydantic.BaseModel):
    """Запрос на удаление чата"""

    id: int = pydantic.Field(..., gt=0)


class DeleteChatResponse(pydantic.BaseModel):
    """Ответ при успешном удалении чата"""

    success: bool = True
