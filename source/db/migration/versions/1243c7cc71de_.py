"""empty message

Revision ID: 1243c7cc71de
Revises: 9f4645ade006
Create Date: 2024-05-02 08:04:18.688411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1243c7cc71de'
down_revision: Union[str, None] = '9f4645ade006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('client', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client', 'is_active')
    op.drop_column('car', 'is_active')
    # ### end Alembic commands ###