"""agregar ultimas columnas a tabla posteos

Revision ID: 109b89fa6ca9
Revises: 3bf91915377b
Create Date: 2023-01-13 15:12:57.409545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '109b89fa6ca9'
down_revision = '3bf91915377b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posteos', sa.Column(
        'publicado', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posteos', sa.Column(
        'creado', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posteos', 'publicado')
    op.drop_column('posteos', 'creado')
    pass
