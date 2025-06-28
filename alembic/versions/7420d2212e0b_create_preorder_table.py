"""create PreOrder table

Revision ID: 7420d2212e0b
Revises: 94e91b60f7a0
Create Date: 2025-06-26 16:44:01.892773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7420d2212e0b'
down_revision: Union[str, None] = '94e91b60f7a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('PreOrder',
    sa.Column('dish_id', sa.Uuid(), nullable=False),
    sa.Column('reservation_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['dish_id'], ['menus.id'], ),
    sa.ForeignKeyConstraint(['reservation_id'], ['reservations.id'], ),
    sa.PrimaryKeyConstraint('dish_id', 'reservation_id')
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('PreOrder')
