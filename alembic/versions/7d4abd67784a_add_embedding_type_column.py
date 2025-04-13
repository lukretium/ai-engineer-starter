"""add embedding_type column

Revision ID: 7d4abd67784a
Revises: d06308dd06df
Create Date: 2024-04-13 15:03:56.545450

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7d4abd67784a"
down_revision: Union[str, None] = "d06308dd06df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add embedding_type column
    op.add_column(
        "documents",
        sa.Column("embedding_type", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    # Remove embedding_type column
    op.drop_column("documents", "embedding_type")
