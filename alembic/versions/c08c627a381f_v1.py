"""v1

Revision ID: c08c627a381f
Revises: 
Create Date: 2022-07-17 17:46:27.272021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c08c627a381f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_login_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('email'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('project',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('owner', sa.String(length=36), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('deploy_at', sa.DateTime(), nullable=True),
    sa.Column('deploy_by', sa.String(length=36), nullable=True),
    sa.Column('type', sa.SmallInteger(), nullable=False),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['deploy_by'], ['user.uuid'], ),
    sa.ForeignKeyConstraint(['owner'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project')
    op.drop_table('user')
    # ### end Alembic commands ###