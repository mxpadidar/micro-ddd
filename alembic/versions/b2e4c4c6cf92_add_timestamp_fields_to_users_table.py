"""add timestamp fields to users table

Revision ID: b2e4c4c6cf92
Revises: 3f867f5ccb4b
Create Date: 2024-04-19 19:42:31.210011

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "b2e4c4c6cf92"
down_revision: Union[str, None] = "3f867f5ccb4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        schema="auth",
    )
    op.add_column(
        "users",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        schema="auth",
    )
    op.add_column(
        "users",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        schema="auth",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "deleted_at", schema="auth")
    op.drop_column("users", "updated_at", schema="auth")
    op.drop_column("users", "created_at", schema="auth")
    # ### end Alembic commands ###
