"""empty message

Revision ID: 45a638ee43c6
Revises: 
Create Date: 2024-05-30 02:11:40.417938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45a638ee43c6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('second_name', sa.String(length=64), nullable=False),
    sa.Column('patronymic', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_id'), 'client', ['id'], unique=False)
    op.create_table('detail_type',
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_detail_type_id'), 'detail_type', ['id'], unique=False)
    op.create_table('model',
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_model_id'), 'model', ['id'], unique=False)
    op.create_table('test_model_1000',
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('some_string', sa.String(length=128), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('fake_unique', sa.String(length=64), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_model_1000_id'), 'test_model_1000', ['id'], unique=False)
    op.create_table('test_model_10000',
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('some_string', sa.String(length=128), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('fake_unique', sa.String(length=64), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_model_10000_id'), 'test_model_10000', ['id'], unique=False)
    op.create_table('test_model_100000',
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('some_string', sa.String(length=128), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('fake_unique', sa.String(length=64), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_model_100000_id'), 'test_model_100000', ['id'], unique=False)
    op.create_table('work',
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('time_cost', sa.DateTime(timezone=True), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_work_id'), 'work', ['id'], unique=False)
    op.create_table('car',
    sa.Column('model_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['model_id'], ['model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_car_id'), 'car', ['id'], unique=False)
    op.create_table('detail',
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['model_id'], ['model.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['detail_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_detail_id'), 'detail', ['id'], unique=False)
    op.create_table('client_xref_car',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_xref_car_id'), 'client_xref_car', ['id'], unique=False)
    op.create_table('order',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('speedometer', sa.Float(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    op.create_table('order_xref_detail',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('detail_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['detail_id'], ['detail.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_xref_detail_id'), 'order_xref_detail', ['id'], unique=False)
    op.create_table('order_xref_work',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('work_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['work_id'], ['work.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_xref_work_id'), 'order_xref_work', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_xref_work_id'), table_name='order_xref_work')
    op.drop_table('order_xref_work')
    op.drop_index(op.f('ix_order_xref_detail_id'), table_name='order_xref_detail')
    op.drop_table('order_xref_detail')
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_client_xref_car_id'), table_name='client_xref_car')
    op.drop_table('client_xref_car')
    op.drop_index(op.f('ix_detail_id'), table_name='detail')
    op.drop_table('detail')
    op.drop_index(op.f('ix_car_id'), table_name='car')
    op.drop_table('car')
    op.drop_index(op.f('ix_work_id'), table_name='work')
    op.drop_table('work')
    op.drop_index(op.f('ix_test_model_100000_id'), table_name='test_model_100000')
    op.drop_table('test_model_100000')
    op.drop_index(op.f('ix_test_model_10000_id'), table_name='test_model_10000')
    op.drop_table('test_model_10000')
    op.drop_index(op.f('ix_test_model_1000_id'), table_name='test_model_1000')
    op.drop_table('test_model_1000')
    op.drop_index(op.f('ix_model_id'), table_name='model')
    op.drop_table('model')
    op.drop_index(op.f('ix_detail_type_id'), table_name='detail_type')
    op.drop_table('detail_type')
    op.drop_index(op.f('ix_client_id'), table_name='client')
    op.drop_table('client')
    # ### end Alembic commands ###
