"""Add logo column to business table

Revision ID: add_business_logo
Revises:
Create Date: 2024-03-28 12:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "add_business_logo"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add logo column to business table
    op.add_column("business", sa.Column("logo", sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    # Remove logo column from business table
    op.drop_column("business", "logo")
