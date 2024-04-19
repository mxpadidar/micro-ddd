import sqlalchemy as sa

from shared.db_setup import registry

users = sa.Table(
    "users",
    registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String, unique=True),
    sa.Column("hashed_password", sa.String),
    sa.Column("is_active", sa.Boolean),
    sa.Column("is_superuser", sa.Boolean),
    sa.Column("created_at", sa.DateTime(timezone=True)),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    schema="auth",
)
