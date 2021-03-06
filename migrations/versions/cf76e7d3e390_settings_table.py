"""settings table

Revision ID: cf76e7d3e390
Revises: 6ce7dde88ddb
Create Date: 2020-06-27 14:18:37.144610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf76e7d3e390'
down_revision = '6ce7dde88ddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('needs_percentage', sa.Float(), nullable=True),
    sa.Column('wants_percentage', sa.Float(), nullable=True),
    sa.Column('savings_percentage', sa.Float(), nullable=True),
    sa.Column('income', sa.Float(), nullable=True),
    sa.Column('effective_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('settings')
    # ### end Alembic commands ###
