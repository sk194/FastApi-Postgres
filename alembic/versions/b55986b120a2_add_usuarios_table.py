"""add usuarios table

Revision ID: b55986b120a2
Revises: b9e74452cb52
Create Date: 2023-01-12 21:28:07.713142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b55986b120a2'
down_revision = 'b9e74452cb52'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('usuarios',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('creado', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('usuarios')
    pass
