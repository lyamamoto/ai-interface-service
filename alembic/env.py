from alembic import context
from dotenv import load_dotenv
#from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool

#from app import Base

# Import models for Alembic autogeneration
#target_metadata = Base.metadata
target_metadata = None

config = context.config
#fileConfig(config.config_file_name)

load_dotenv()
sqlalchemy_url = f"postgresql+psycopg2://{os.getenv('postgres.user')}:{os.getenv('postgres.password')}@{os.getenv('postgres.host')}/{os.getenv('postgres.db')}"
config.set_main_option("sqlalchemy.url", sqlalchemy_url)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()