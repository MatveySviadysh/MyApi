"""empty message

Revision ID: 84d23919a1a7
Revises: 151dc64b0ed5
Create Date: 2024-11-07 17:18:26.620138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84d23919a1a7'
down_revision: Union[str, None] = '151dc64b0ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
