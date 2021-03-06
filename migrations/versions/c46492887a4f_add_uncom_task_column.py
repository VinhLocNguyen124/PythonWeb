"""add uncom_task Column

Revision ID: c46492887a4f
Revises: 457683f47765
Create Date: 2020-07-09 13:07:20.351304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c46492887a4f'
down_revision = '457683f47765'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('uncom_task', sa.Integer(), nullable=False))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'project', ['project_id'], ['project_id'])
    op.create_foreign_key(None, 'task', 'priority', ['priority_id'], ['priority_id'])
    op.drop_column('task', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'user', ['user_id'], ['user_id'])
    op.drop_column('project', 'uncom_task')
    # ### end Alembic commands ###
