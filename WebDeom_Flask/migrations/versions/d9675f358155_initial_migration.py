"""initial migration

Revision ID: d9675f358155
Revises: fbe630b5fbdb
Create Date: 2018-05-13 00:52:05.623353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9675f358155'
down_revision = 'fbe630b5fbdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
   ### op.alter_column('users', 'psd', ###
    ###           existing_type=sa.VARCHAR(length=40), ###
     ###          type_=sa.String(length=128), ###
     ###          existing_nullable=True) ###
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
	pass
    ###op.alter_column('users', 'psd',
    ###           existing_type=sa.String(length=128),###
    ###           type_=sa.VARCHAR(length=40),###
     ###          existing_nullable=True)	   ###
    # ### end Alembic commands ###
