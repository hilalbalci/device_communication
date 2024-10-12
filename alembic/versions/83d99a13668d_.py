"""empty message

Revision ID: 83d99a13668d
Revises: 
Create Date: 2024-10-11 10:35:08.501047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83d99a13668d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_devices_name', 'name'),
    )
    op.create_table(
        'device_locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('device_locations')
    op.drop_table('devices')
