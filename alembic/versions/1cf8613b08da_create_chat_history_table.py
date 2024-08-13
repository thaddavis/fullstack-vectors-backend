"""create chat_history table

Revision ID: 1cf8613b08da
Revises: 7c57c0bf4b0b
Create Date: 2024-08-12 02:01:14.518716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cf8613b08da'
down_revision: Union[str, None] = '7c57c0bf4b0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'chat_history',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('session_id', sa.UUID),
        sa.Column('message', sa.JSON),
        sa.Column('created_at', sa.DateTime(timezone=True), default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('chat_history')
