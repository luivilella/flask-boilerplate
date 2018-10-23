"""empty message

Revision ID: 40ebf08c6481
Revises:
Create Date: 2018-10-23 21:50:54.212069

"""
from alembic import op
import sqlalchemy as sa


revision = '40ebf08c6481'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_update', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('passwd', sa.String(length=100), nullable=False),
        sa.Column('fullname', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_users_username'), 'users', ['username'], unique=True
    )


def downgrade():
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
