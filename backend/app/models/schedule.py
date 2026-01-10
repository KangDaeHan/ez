import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SchedulePriority(str, Enum):
    """일정 우선순위"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DEFAULT = "default"


class ScheduleRepeatType(str, Enum):
    """일정 반복 타입"""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class ReminderType(str, Enum):
    """알림 타입"""

    NOTIFICATION = "notification"
    EMAIL = "email"


class Schedule(Base):
    """일정 모델"""

    __tablename__ = "schedules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    all_day: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[SchedulePriority] = mapped_column(
        SQLEnum(SchedulePriority, values_callable=lambda x: [e.value for e in x]),
        default=SchedulePriority.DEFAULT
    )
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    repeat: Mapped[ScheduleRepeatType] = mapped_column(
        SQLEnum(ScheduleRepeatType, values_callable=lambda x: [e.value for e in x]),
        default=ScheduleRepeatType.NONE
    )
    repeat_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user = relationship("User", back_populates="schedules")
    reminders = relationship(
        "ScheduleReminder", back_populates="schedule", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Schedule {self.title}>"


class ScheduleReminder(Base):
    """일정 알림 모델"""

    __tablename__ = "schedule_reminders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    schedule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False, index=True
    )
    reminder_type: Mapped[ReminderType] = mapped_column(
        SQLEnum(ReminderType, values_callable=lambda x: [e.value for e in x]),
        default=ReminderType.NOTIFICATION
    )
    minutes_before: Mapped[int] = mapped_column(Integer, default=30)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    schedule = relationship("Schedule", back_populates="reminders")

    def __repr__(self) -> str:
        return f"<ScheduleReminder {self.minutes_before}min>"

