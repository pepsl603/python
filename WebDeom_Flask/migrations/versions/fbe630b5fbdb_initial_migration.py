"""initial migration

Revision ID: fbe630b5fbdb
Revises: b27ef17b311d
Create Date: 2018-05-13 00:38:29.520832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbe630b5fbdb'
down_revision = 'b27ef17b311d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass#op.create_unique_constraint(None, 'users', ['mail'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass#op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
