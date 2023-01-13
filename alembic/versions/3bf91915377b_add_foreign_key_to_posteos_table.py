"""add foreign-key to posteos table

Revision ID: 3bf91915377b
Revises: b55986b120a2
Create Date: 2023-01-12 22:36:13.256147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bf91915377b'
down_revision = 'b55986b120a2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posteos', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posteo_usuarios_fk', source_table="posteos", referent_table="usuarios",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posteo_usuario_fk', table_name="posteos")
    op.drop_column('posteos', 'owner_id')
    
    pass
