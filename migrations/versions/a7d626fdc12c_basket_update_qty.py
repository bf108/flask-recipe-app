"""basket update qty

Revision ID: a7d626fdc12c
Revises: 23fd44bdbb1e
Create Date: 2022-10-17 21:44:25.930691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7d626fdc12c'
down_revision = '23fd44bdbb1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('basket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quatity', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('basket', schema=None) as batch_op:
        batch_op.drop_column('quatity')

    # ### end Alembic commands ###
