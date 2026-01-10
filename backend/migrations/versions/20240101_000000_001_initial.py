"""Initial migration - create users, schedules, schedule_reminders tables

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    # Create enum types
    schedule_priority = postgresql.ENUM(
        "high", "medium", "low", "default", name="schedulepriority", create_type=True
    )
    schedule_repeat_type = postgresql.ENUM(
        "none", "daily", "weekly", "monthly", "yearly", name="schedulerepeattype", create_type=True
    )
    reminder_type = postgresql.ENUM(
        "notification", "email", name="remindertype", create_type=True
    )

    # Create schedules table
    op.create_table(
        "schedules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("all_day", sa.Boolean(), nullable=False, default=False),
        sa.Column("priority", schedule_priority, nullable=False, default="default"),
        sa.Column("color", sa.String(20), nullable=True),
        sa.Column("location", sa.String(500), nullable=True),
        sa.Column("image_url", sa.String(500), nullable=True),
        sa.Column("repeat", schedule_repeat_type, nullable=False, default="none"),
        sa.Column("repeat_end_date", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_schedules_user_id"), "schedules", ["user_id"], unique=False)
    op.create_index(op.f("ix_schedules_start_date"), "schedules", ["start_date"], unique=False)

    # Create schedule_reminders table
    op.create_table(
        "schedule_reminders",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reminder_type", reminder_type, nullable=False, default="notification"),
        sa.Column("minutes_before", sa.Integer(), nullable=False, default=30),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["schedule_id"], ["schedules.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_schedule_reminders_schedule_id"),
        "schedule_reminders",
        ["schedule_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_schedule_reminders_schedule_id"), table_name="schedule_reminders")
    op.drop_table("schedule_reminders")
    op.drop_index(op.f("ix_schedules_start_date"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_user_id"), table_name="schedules")
    op.drop_table("schedules")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS remindertype")
    op.execute("DROP TYPE IF EXISTS schedulerepeattype")
    op.execute("DROP TYPE IF EXISTS schedulepriority")

