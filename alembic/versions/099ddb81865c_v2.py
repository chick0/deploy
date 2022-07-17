"""v2

Revision ID: 099ddb81865c
Revises: c08c627a381f
Create Date: 2022-07-17 19:29:31.404289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '099ddb81865c'
down_revision = 'c08c627a381f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deploy_token',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('project', sa.String(length=36), nullable=True),
    sa.Column('create_by', sa.String(length=36), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.Column('write', sa.Boolean(), nullable=True),
    sa.Column('delete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['create_by'], ['user.uuid'], ),
    sa.ForeignKeyConstraint(['project'], ['project.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deploy_token')
    # ### end Alembic commands ###