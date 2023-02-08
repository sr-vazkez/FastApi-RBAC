"""04 adds indexs in all tables.

Revision ID: b3da57eb0104
Revises: 0091ea2e56fb
Create Date: 2022-11-05 11:47:08.828351

"""
from alembic import op
import sqlalchemy as sa  # noqa


# revision identifiers, used by Alembic.
revision = "b3da57eb0104"
down_revision = "0091ea2e56fb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Commands auto generated by Alembic - please adjust."""
    op.create_index(op.f("ix_actions_id"), "actions", ["id"], unique=False)
    op.create_index(op.f("ix_modules_id"), "modules", ["id"], unique=False)
    op.create_index(op.f("ix_role_actions_id"), "role_actions", ["id"], unique=False)
    op.create_index(op.f("ix_roles_id"), "roles", ["id"], unique=False)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Commands auto generated by Alembic - please adjust."""
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_roles_id"), table_name="roles")
    op.drop_index(op.f("ix_role_actions_id"), table_name="role_actions")
    op.drop_index(op.f("ix_modules_id"), table_name="modules")
    op.drop_index(op.f("ix_actions_id"), table_name="actions")
    # ### end Alembic commands ###