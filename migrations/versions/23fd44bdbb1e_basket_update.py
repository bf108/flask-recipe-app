"""basket update

Revision ID: 23fd44bdbb1e
Revises: a1bce827c72a
Create Date: 2022-10-17 21:40:58.984290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23fd44bdbb1e'
down_revision = 'a1bce827c72a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('basket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipe_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('uq_basket_basket_title', type_='unique')
        batch_op.create_foreign_key(batch_op.f('fk_basket_recipe_id_recipes'), 'recipes', ['recipe_id'], ['id'], ondelete='CASCADE')
        batch_op.drop_column('basket_title')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('basket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('basket_title', sa.VARCHAR(), nullable=False))
        batch_op.drop_constraint(batch_op.f('fk_basket_recipe_id_recipes'), type_='foreignkey')
        batch_op.create_unique_constraint('uq_basket_basket_title', ['basket_title'])
        batch_op.drop_column('recipe_id')

    # ### end Alembic commands ###