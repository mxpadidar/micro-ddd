"""add avatar file id to user

Revision ID: 1de4d78e6665
Revises: ce473f876d27
Create Date: 2024-04-26 15:20:38.372800

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "1de4d78e6665"
down_revision: Union[str, None] = "ce473f876d27"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("avatar_file_id", sa.Integer(), nullable=True), schema="auth"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "avatar_file_id", schema="auth")
    # ### end Alembic commands ###