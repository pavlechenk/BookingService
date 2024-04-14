"""Add users, rooms, hotels and bookings migration

Revision ID: ed68d352abd5
Revises: 
Create Date: 2024-02-03 22:59:34.009286

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ed68d352abd5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
