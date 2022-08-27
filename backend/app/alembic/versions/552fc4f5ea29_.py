"""empty message

Revision ID: 552fc4f5ea29
Revises: 68601acb67ff
Create Date: 2022-08-27 00:16:45.752501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '552fc4f5ea29'
down_revision = '68601acb67ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('commande', sa.Column('qty_fixed', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('commande', 'qty_fixed')
    # ### end Alembic commands ###
