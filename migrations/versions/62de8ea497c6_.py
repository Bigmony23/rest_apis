"""empty message

Revision ID: 62de8ea497c6
Revises: 5239371fa9ca
Create Date: 2024-10-24 19:24:21.425344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62de8ea497c6'
down_revision = '5239371fa9ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
