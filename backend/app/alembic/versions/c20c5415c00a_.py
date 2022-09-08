"""empty message

Revision ID: c20c5415c00a
Revises: 1f5ac7f58bbe
Create Date: 2022-09-08 00:34:12.661032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c20c5415c00a'
down_revision = '1f5ac7f58bbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_holdedorder_id', table_name='holdedorder')
    op.drop_column('holdedorder', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('holdedorder', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_index('ix_holdedorder_id', 'holdedorder', ['id'], unique=False)
    # ### end Alembic commands ###