"""Initial migration

Revision ID: 9c21b2d2f834
Revises:
Create Date: 2026-01-26 16:15:35.161115

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = '9c21b2d2f834'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('chats',
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=True, start=1), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chats'))
    )
    op.create_table('messages',
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('text', sa.String(length=5000), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=True, start=1), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], name=op.f('fk_messages_chat_id_chats'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('messages')
    op.drop_table('chats')
