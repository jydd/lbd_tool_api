"""empty message

Revision ID: 0de11cd433cd
Revises: 86377875c826
Create Date: 2020-12-02 16:07:23.164430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0de11cd433cd'
down_revision = '86377875c826'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tel', sa.String(length=11), nullable=True),
    sa.Column('nickname', sa.String(length=255), nullable=True),
    sa.Column('headimgurl', sa.String(length=255), nullable=True),
    sa.Column('mp_openid', sa.String(length=255), nullable=True),
    sa.Column('min_openid', sa.String(length=255), nullable=True),
    sa.Column('unionid', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_member_created_at'), 'member', ['created_at'], unique=False)
    op.add_column('netease', sa.Column('mid', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'netease', 'member', ['mid'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'netease', type_='foreignkey')
    op.drop_column('netease', 'mid')
    op.drop_index(op.f('ix_member_created_at'), table_name='member')
    op.drop_table('member')
    # ### end Alembic commands ###
