"""remove category and and add bucket in files table

Revision ID: e84f03e4ede7
Revises: 1918fb39c7f6
Create Date: 2024-05-04 21:06:13.238491

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "e84f03e4ede7"
down_revision: Union[str, None] = "1918fb39c7f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "files", sa.Column("bucket", sa.String(), nullable=True), schema="storage"
    )
    op.drop_constraint("unique_file", "files", schema="storage", type_="unique")
    op.create_unique_constraint(
        "unique_file", "files", ["bucket", "name"], schema="storage"
    )
    op.drop_column("files", "category", schema="storage")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "files",
        sa.Column("category", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="storage",
    )
    op.drop_constraint("unique_file", "files", schema="storage", type_="unique")
    op.create_unique_constraint(
        "unique_file", "files", ["category", "name"], schema="storage"
    )
    op.drop_column("files", "bucket", schema="storage")
    # ### end Alembic commands ###
