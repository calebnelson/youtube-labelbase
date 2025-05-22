"""create outputs table

Revision ID: 8f7d9e6c5b4a
Revises: b2af9ab0f7b3
Create Date: 2024-03-21

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8f7d9e6c5b4a'
down_revision = 'b2af9ab0f7b3'  # Points to the last migration
branch_labels = None
depends_on = None

def upgrade():
    # Create outputs table
    op.create_table(
        'outputs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('video_id', sa.Integer(), nullable=False),
        sa.Column('prompt_id', sa.String(), nullable=False),
        sa.Column('llm_output', sa.String(), nullable=False),
        sa.Column('run_date', sa.DateTime(), nullable=False),
        sa.Column('time_to_generate', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['prompt_id'], ['prompts.id'], ),
        sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_outputs_id'), 'outputs', ['id'], unique=False)

    # Remove video_id from prompts table
    op.drop_constraint('prompts_video_id_fkey', 'prompts', type_='foreignkey')
    op.drop_column('prompts', 'video_id')

    # Remove output column from prompts table
    op.drop_column('prompts', 'output')

def downgrade():
    # Add back video_id to prompts table
    op.add_column('prompts', sa.Column('video_id', sa.Integer(), nullable=True))
    op.create_foreign_key('prompts_video_id_fkey', 'prompts', 'videos', ['video_id'], ['id'])

    # Add back output column to prompts table
    op.add_column('prompts', sa.Column('output', postgresql.JSON(astext_type=sa.Text()), nullable=True))

    # Drop outputs table
    op.drop_index(op.f('ix_outputs_id'), table_name='outputs')
    op.drop_table('outputs') 