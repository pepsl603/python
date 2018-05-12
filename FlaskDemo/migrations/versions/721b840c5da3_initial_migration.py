"""initial migration

Revision ID: 721b840c5da3
Revises: 
Create Date: 2018-05-11 22:57:49.472822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '721b840c5da3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('mail', sa.String(length=200)))
    op.add_column('users', sa.Column('psd', sa.String(length=40)))
    #op.create_unique_constraint(None, 'users', ['mail'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'psd')
    op.drop_column('users', 'mail')
    # ### end Alembic commands ###