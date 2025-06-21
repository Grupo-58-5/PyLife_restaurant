"""creation user table

Revision ID: 82d30ead0240
Revises: 
Create Date: 2025-06-04 22:16:31.127624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlmodel
import sqlmodel.sql
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '82d30ead0240'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def create_user_table():
    op.create_table('user',
        sa.Column('id', UUID(as_uuid=True),server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False, unique=True),
        sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('role', sa.Enum('ADMIN', 'CLIENT', name='roles'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def upgrade() -> None:
    """Upgrade schema."""
    create_user_table()
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS roles;")
