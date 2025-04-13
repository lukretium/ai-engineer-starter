"""create documents table

Revision ID: d06308dd06df
Revises: daa2443e0576
Create Date: 2025-04-13 15:03:56.545450

"""

from collections.abc import Sequence

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d06308dd06df"
down_revision: str | None = "daa2443e0576"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create the vector extension if it doesn't exist
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create documents table
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("document_metadata", postgresql.JSONB(), nullable=True),
        sa.Column("embedding", Vector(1536), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create index on id
    op.create_index("ix_documents_id", "documents", ["id"], unique=False)


def downgrade() -> None:
    # Drop the table and index
    op.drop_index("ix_documents_id", table_name="documents")
    op.drop_table("documents")

    # Drop the vector extension
    op.execute("DROP EXTENSION IF EXISTS vector")
