"""add task isCompleted column

Revision ID: c61ba0a46da0
Revises: 6d257f9a9ec9
Create Date: 2020-07-09 07:51:51.460329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c61ba0a46da0'
down_revision = '6d257f9a9ec9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'task', 'priority', ['priority_id'], ['priority_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    # ### end Alembic commands ###
