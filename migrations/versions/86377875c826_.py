"""empty message

Revision ID: 86377875c826
Revises: 9e4bbb30f2e8
Create Date: 2020-11-30 15:57:41.089723

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '86377875c826'
down_revision = '9e4bbb30f2e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('netease', 'messages')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('netease', sa.Column('messages', mysql.VARCHAR(length=255), nullable=True))
    # ### end Alembic commands ###
