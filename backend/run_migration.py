from alembic import command
from alembic.config import Config


def run_migration():
    # Create Alembic configuration
    alembic_cfg = Config("alembic.ini")

    # Run the migration
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    run_migration()
