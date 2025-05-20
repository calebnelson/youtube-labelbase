"""Add user_id to prompts

Revision ID: b2af9ab0f7b3
Revises: 17da819afbe3
Create Date: 2025-05-19 19:32:04.352550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2af9ab0f7b3'
down_revision: Union[str, None] = '17da819afbe3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add user_id column to prompts table
    op.add_column('prompts', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'prompts_user_id_fkey',
        'prompts', 'users',
        ['user_id'], ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove foreign key constraint and user_id column
    op.drop_constraint('prompts_user_id_fkey', 'prompts', type_='foreignkey')
    op.drop_column('prompts', 'user_id')
