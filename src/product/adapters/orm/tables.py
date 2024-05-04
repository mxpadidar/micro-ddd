import sqlalchemy as sa

from shared.db_setup import registry

products = sa.Table(
    "products",
    registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("price", sa.Float, nullable=False),
    sa.Column("avatar_file_id", sa.Integer, nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True)),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    schema="product",
)
