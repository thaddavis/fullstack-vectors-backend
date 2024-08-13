"""rename is_suspicious column to similarity_score

Revision ID: e593a644355a
Revises: a449e5112ff5
Create Date: 2024-08-13 16:57:00.495518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e593a644355a'
down_revision: Union[str, None] = 'a449e5112ff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the column
    op.alter_column('logins', 'is_suspicious', new_column_name='similarity_score')


def downgrade() -> None:
    # Revert the column name first
    op.alter_column('logins', 'similarity_score', new_column_name='is_suspicious')
