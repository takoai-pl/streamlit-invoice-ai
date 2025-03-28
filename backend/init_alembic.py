from alembic import command
from alembic.config import Config


def init_alembic():
    # Create Alembic configuration
    alembic_cfg = Config("alembic.ini")

    # Initialize Alembic
    command.init(alembic_cfg, "migrations")


if __name__ == "__main__":
    init_alembic()
