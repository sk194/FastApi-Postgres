"""add contenido column to posteos table

Revision ID: b9e74452cb52
Revises: f1c59e2eaf3b
Create Date: 2023-01-12 20:32:22.366709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9e74452cb52'
down_revision = 'f1c59e2eaf3b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posteos', sa.Column('contenido', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posteos', 'contenido')
    pass
