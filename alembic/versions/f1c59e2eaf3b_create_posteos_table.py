"""create posteos table

Revision ID: f1c59e2eaf3b
Revises: 
Create Date: 2023-01-12 19:36:10.892764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1c59e2eaf3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posteos', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
                    , sa.Column('titulo', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posteos')
    pass
