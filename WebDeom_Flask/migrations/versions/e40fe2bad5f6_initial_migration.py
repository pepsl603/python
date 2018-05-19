"""initial migration

Revision ID: e40fe2bad5f6
Revises: 64d046f7b263
Create Date: 2018-05-18 23:32:42.816563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e40fe2bad5f6'
down_revision = '64d046f7b263'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_users_old_20180518')
    op.drop_table('_users_old_20180518_1')
    op.add_column('users', sa.Column('user_pic', sa.LargeBinary(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_pic')
    op.create_table('_users_old_20180518_1',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=200), nullable=True),
    sa.Column('psd', sa.VARCHAR(length=128), nullable=True),
    sa.Column('mail', sa.VARCHAR(length=200), nullable=True),
    sa.Column('recdate', sa.DATETIME(), nullable=True),
    sa.Column('role_id', sa.INTEGER(), nullable=True),
    sa.Column('phonenum', sa.VARCHAR(length=20), nullable=True),
    sa.Column('confirmed', sa.BOOLEAN(), nullable=True),
    sa.Column('about_me', sa.TEXT(), nullable=True),
    sa.Column('last_seen', sa.DATETIME(), nullable=True),
    sa.Column('location', sa.VARCHAR(length=200), nullable=True),
    sa.Column('name', sa.VARCHAR(length=40), nullable=True),
    sa.Column('avatar_hash', sa.VARCHAR(length=32), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('_users_old_20180518',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=200), nullable=True),
    sa.Column('psd', sa.VARCHAR(length=128), nullable=True),
    sa.Column('mail', sa.VARCHAR(length=200), nullable=True),
    sa.Column('recdate', sa.DATETIME(), nullable=True),
    sa.Column('role_id', sa.INTEGER(), nullable=True),
    sa.Column('phonenum', sa.VARCHAR(length=20), nullable=True),
    sa.Column('confirmed', sa.BOOLEAN(), nullable=True),
    sa.Column('about_me', sa.TEXT(), nullable=True),
    sa.Column('last_seen', sa.DATETIME(), nullable=True),
    sa.Column('location', sa.VARCHAR(length=200), nullable=True),
    sa.Column('name', sa.VARCHAR(length=40), nullable=True),
    sa.Column('avatar_hash', sa.VARCHAR(length=32), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
