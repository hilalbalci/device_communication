"""add soft delete

Revision ID: 2bb8c365f665
Revises: 83d99a13668d
Create Date: 2024-10-12 12:53:32.879675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bb8c365f665'
down_revision: Union[str, None] = '83d99a13668d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('devices', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('devices', 'is_deleted')