"""empty message

Revision ID: 926755d1e11e
Revises: febcd7f5d67e
Create Date: 2024-10-30 17:20:52.111428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '926755d1e11e'
down_revision: Union[str, None] = 'febcd7f5d67e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.VARCHAR(), nullable=False))
    # ### end Alembic commands ###