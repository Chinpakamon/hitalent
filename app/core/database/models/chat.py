import sqlalchemy
from sqlalchemy import orm

from app.core.database import Base, mixins


class Chat(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    __tablename__ = "chats"

    title: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(200), nullable=False)

    messages = orm.relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )
