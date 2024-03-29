"""05 cambiando status por is active.

Revision ID: 67c2f857f142
Revises: b3da57eb0104
Create Date: 2022-11-14 10:55:00.107511

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "67c2f857f142"
down_revision = "b3da57eb0104"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Commands auto generated by Alembic - please adjust."""
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False))
    op.drop_column("users", "status")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Commands auto generated by Alembic - please adjust."""
    op.add_column(
        "users",
        sa.Column(
            "status",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###
