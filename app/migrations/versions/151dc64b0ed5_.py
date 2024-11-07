"""empty message

Revision ID: 151dc64b0ed5
Revises: c3d124454000
Create Date: 2024-11-07 17:17:31.142739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '151dc64b0ed5'
down_revision: Union[str, None] = 'c3d124454000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
