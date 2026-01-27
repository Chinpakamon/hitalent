import sqlalchemy
from sqlalchemy import orm

from app.core.database import Base, mixins


class Message(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    __tablename__ = "messages"

    chat_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey("chats.id", ondelete="CASCADE")
    )
    text: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(5000), nullable=False)

    chat = orm.relationship("Chat", back_populates="messages")
