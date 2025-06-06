"""insert admin user

Revision ID: d9979ed1cf09
Revises: 82d30ead0240
Create Date: 2025-06-05 12:02:48.556141

"""
from typing import Sequence, Union

from alembic import op
from bcrypt import checkpw,hashpw,gensalt
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9979ed1cf09'
down_revision: Union[str, None] = '82d30ead0240'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    password: str = 'password'
    encoded = hashpw(
        password.encode('utf-8'),
        gensalt()
    )

    decoded = encoded.decode('utf-8')
    sql_query = f""" INSERT INTO public."user"(name, email, password, role) VALUES ('Luigi Bastidas', 'luigi@test.com', '{decoded}', 'ADMIN');"""
    op.execute(sql_query)


def downgrade() -> None:
    """Downgrade schema."""
    sql_query = """DELETE FROM public."user" WHERE email = 'luigi@test.com';"""
    op.execute(sql_query)
