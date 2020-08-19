"""add uncom_task Column

Revision ID: db1f8f9bdbc3
Revises: c46492887a4f
Create Date: 2020-07-09 13:08:04.737191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db1f8f9bdbc3'
down_revision = 'c46492887a4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('uncom_task', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'priority', ['priority_id'], ['priority_id'])
    op.create_foreign_key(None, 'task', 'project', ['project_id'], ['project_id'])
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
