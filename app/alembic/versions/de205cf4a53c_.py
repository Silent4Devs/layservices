"""empty message

Revision ID: de205cf4a53c
Revises: 2e23df6e5700
Create Date: 2025-04-16 13:25:40.954370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de205cf4a53c'
down_revision: Union[str, None] = '2e23df6e5700'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
