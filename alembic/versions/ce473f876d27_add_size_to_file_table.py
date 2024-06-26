"""add size to file table

Revision ID: ce473f876d27
Revises: 96e55cd5f195
Create Date: 2024-04-20 23:31:31.491050

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "ce473f876d27"
down_revision: Union[str, None] = "96e55cd5f195"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "files", sa.Column("mime_type", sa.String(), nullable=True), schema="storage"
    )
    op.add_column(
        "files", sa.Column("size", sa.Integer(), nullable=True), schema="storage"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("files", "size", schema="storage")
    op.drop_column("files", "mime_type", schema="storage")
    # ### end Alembic commands ###
