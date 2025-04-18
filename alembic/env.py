import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models.base import Base
from app.models import user, product, inventory_entry, pricing_rules,alert
from dotenv import load_dotenv
import os
load_dotenv()

# Debug print to see if it's loading
print("DATABASE_URL = ", os.getenv("DATABASE_URL"))
# Load env variables
from app.config.config import settings

# this is the Alembic Config object
config = context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# your DATABASE_URL from settings
DATABASE_URL = settings.DATABASE_URL

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
