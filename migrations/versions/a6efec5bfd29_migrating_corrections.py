"""migrating corrections

Revision ID: a6efec5bfd29
Revises: a98ec6b1dbe2
Create Date: 2023-11-19 10:51:40.254816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6efec5bfd29'
down_revision = 'a98ec6b1dbe2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_password_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_password_key', ['password'])

    # ### end Alembic commands ###
