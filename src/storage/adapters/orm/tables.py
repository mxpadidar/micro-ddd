import sqlalchemy as sa

from shared.db_setup import registry

files = sa.Table(
    "files",
    registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("bucket", sa.String),
    sa.Column("name", sa.String),
    sa.Column("mime_type", sa.String),
    sa.Column("size", sa.Integer),
    sa.Column("used", sa.Boolean, default=False),
    sa.Column("created_at", sa.DateTime(timezone=True)),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    sa.UniqueConstraint("bucket", "name", name="unique_file"),
    schema="storage",
)
