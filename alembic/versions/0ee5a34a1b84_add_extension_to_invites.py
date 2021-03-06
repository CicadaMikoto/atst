"""add extension to invites

Revision ID: 0ee5a34a1b84
Revises: 4a3122ffe898
Create Date: 2019-09-09 16:16:32.018776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ee5a34a1b84' # pragma: allowlist secret
down_revision = '4a3122ffe898' # pragma: allowlist secret
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application_invitations', sa.Column('phone_ext', sa.String(), nullable=True))
    op.add_column('portfolio_invitations', sa.Column('phone_ext', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('portfolio_invitations', 'phone_ext')
    op.drop_column('application_invitations', 'phone_ext')
    # ### end Alembic commands ###
