"""alter is_suspicious column of logins table

Revision ID: a449e5112ff5
Revises: d54c82f29baa
Create Date: 2024-08-13 16:38:58.891130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a449e5112ff5'
down_revision: Union[str, None] = 'd54c82f29baa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use raw SQL to include the USING clause with custom casting logic
    op.execute("""
        ALTER TABLE logins
        ALTER COLUMN is_suspicious TYPE double precision
        USING CASE 
            WHEN is_suspicious = true THEN 0.0
            ELSE 1.0
        END;
    """)


def downgrade() -> None:
    # Downgrade logic to revert the column back to BOOLEAN with custom casting logic
    op.execute("""
        ALTER TABLE logins
        ALTER COLUMN is_suspicious TYPE BOOLEAN
        USING CASE 
            WHEN is_suspicious = 0.0 THEN true
            ELSE false
        END;
    """)
