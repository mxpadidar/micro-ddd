from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context  # type: ignore
from auth.adapters.orm import tables as auth_tables  # noqa
from shared.db_setup import registry
from shared.settings import POSTGRES_URI
from storage.adapters.orm import tables as storage_tables  # noqa

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", POSTGRES_URI)

target_metadata = registry.metadata


def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            create_type=True,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
