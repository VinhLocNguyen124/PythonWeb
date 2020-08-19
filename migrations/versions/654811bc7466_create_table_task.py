"""create table task

Revision ID: 654811bc7466
Revises: 5fe76dcb62aa
Create Date: 2020-06-18 09:46:51.044272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '654811bc7466'
down_revision = '5fe76dcb62aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('task_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###