"""empty message

Revision ID: b1d36b1c1a35
Revises: a99069e6bf80
Create Date: 2020-11-25 21:44:17.743653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1d36b1c1a35'
down_revision = 'a99069e6bf80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('netease',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netease_created_at'), 'netease', ['created_at'], unique=False)
    op.create_table('netease_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('types', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['netease.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_netease_tasks_created_at'), 'netease_tasks', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_netease_tasks_created_at'), table_name='netease_tasks')
    op.drop_table('netease_tasks')
    op.drop_index(op.f('ix_netease_created_at'), table_name='netease')
    op.drop_table('netease')
    # ### end Alembic commands ###
