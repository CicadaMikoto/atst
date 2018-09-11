"""request_reviews comment column name

Revision ID: 53ab3edd334b
Revises: 777ded5c57a0
Create Date: 2018-09-10 13:29:02.648359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53ab3edd334b'
down_revision = '777ded5c57a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request_reviews', sa.Column('comment', sa.String(), nullable=True))
    op.drop_column('request_reviews', 'comments')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request_reviews', sa.Column('comments', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('request_reviews', 'comment')
    # ### end Alembic commands ###