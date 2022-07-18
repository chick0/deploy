"""v4

Revision ID: c78545df2f8e
Revises: 4abcca9b324e
Create Date: 2022-07-19 01:26:21.418936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c78545df2f8e'
down_revision = '4abcca9b324e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deploy_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project', sa.String(length=36), nullable=True),
    sa.Column('create_by', sa.String(length=36), nullable=True),
    sa.Column('type', sa.SmallInteger(), nullable=False),
    sa.Column('called_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('return_code', sa.Integer(), nullable=False),
    sa.Column('stdout', sa.Text(), nullable=False),
    sa.Column('stderr', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['called_by'], ['deploy_log.id'], ),
    sa.ForeignKeyConstraint(['create_by'], ['user.uuid'], ),
    sa.ForeignKeyConstraint(['project'], ['project.uuid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deploy_log')
    # ### end Alembic commands ###
