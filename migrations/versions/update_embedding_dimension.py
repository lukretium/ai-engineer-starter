"""update embedding dimension

Revision ID: update_embedding_dimension
Revises:
Create Date: 2024-03-21 10:00:00.000000

"""

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

from alembic import op

# revision identifiers, used by Alembic.
revision = "update_embedding_dimension"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop the existing embedding column
    op.drop_column("documents", "embedding")

    # Recreate the embedding column without a fixed dimension
    op.add_column("documents", sa.Column("embedding", Vector(), nullable=True))


def downgrade():
    # Drop the dynamic dimension embedding column
    op.drop_column("documents", "embedding")

    # Recreate the embedding column with fixed dimension (1536 for OpenAI)
    op.add_column("documents", sa.Column("embedding", Vector(1536), nullable=True))
