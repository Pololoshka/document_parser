"""Initial

Revision ID: f2051c50bb89
Revises:
Create Date: 2024-04-06 11:49:20.007762

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f2051c50bb89"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "documents", sa.Column("hash", sa.String(), nullable=False), sa.PrimaryKeyConstraint("hash")
    )
    op.create_table(
        "words",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("words")
    op.drop_table("documents")
    # ### end Alembic commands ###
