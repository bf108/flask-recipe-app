"""basket

Revision ID: a1bce827c72a
Revises: 52366b30aa3d
Create Date: 2022-10-17 21:38:32.311294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1bce827c72a'
down_revision = '52366b30aa3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('basketrecipes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_basketrecipes_basket_id_basket', type_='foreignkey')
        batch_op.drop_column('basket_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('basketrecipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('basket_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('fk_basketrecipes_basket_id_basket', 'basket', ['basket_id'], ['id'])

    # ### end Alembic commands ###