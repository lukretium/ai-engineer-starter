"""update_vector_dimensions

Revision ID: 71ece6175250
Revises: 7d4abd67784a
Create Date: 2025-04-13 15:35:21.712511

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "71ece6175250"
down_revision: Union[str, None] = "7d4abd67784a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
