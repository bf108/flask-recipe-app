"""add recipe and category tables

Revision ID: 54cb2465cda1
Revises: 
Create Date: 2022-09-23 22:23:34.822296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54cb2465cda1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_categories'))
    )
    op.create_table('ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('fk_ingredients_category_id_categories')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ingredients'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ingredients')
    op.drop_table('categories')
    # ### end Alembic commands ###