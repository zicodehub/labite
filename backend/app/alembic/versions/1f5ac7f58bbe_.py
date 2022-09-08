"""empty message

Revision ID: 1f5ac7f58bbe
Revises: 554aee2ba382
Create Date: 2022-09-08 00:32:22.844690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f5ac7f58bbe'
down_revision = '554aee2ba382'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('holdedorder', sa.Column('id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_holdedorder_id'), 'holdedorder', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_holdedorder_id'), table_name='holdedorder')
    op.drop_column('holdedorder', 'id')
    # ### end Alembic commands ###
