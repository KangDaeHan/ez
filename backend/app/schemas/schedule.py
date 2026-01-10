from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.models.schedule import SchedulePriority, ScheduleRepeatType, ReminderType


class ReminderBase(BaseModel):
    """알림 기본 스키마"""
    model_config = ConfigDict(populate_by_name=True)

    reminder_type: ReminderType = Field(default=ReminderType.NOTIFICATION, alias="reminderType", serialization_alias="type")
    minutes_before: int = Field(default=30, ge=0, le=10080, alias="minutesBefore", serialization_alias="minutesBefore")  # 최대 1주


class ReminderCreate(ReminderBase):
    """알림 생성 스키마"""

    pass


class ReminderResponse(ReminderBase):
    """알림 응답 스키마"""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID


class ScheduleBase(BaseModel):
    """일정 기본 스키마"""
    model_config = ConfigDict(populate_by_name=True)

    # 필수값
    title: str = Field(..., min_length=1, max_length=200)
    start_date: datetime = Field(..., alias="startDate", serialization_alias="startDate")
    
    # 옵션값
    end_date: Optional[datetime] = Field(None, alias="endDate", serialization_alias="endDate")
    description: Optional[str] = Field(None, max_length=2000)
    all_day: bool = Field(default=False, alias="allDay", serialization_alias="allDay")
    priority: SchedulePriority = SchedulePriority.DEFAULT
    color: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=500)
    repeat: ScheduleRepeatType = ScheduleRepeatType.NONE
    repeat_end_date: Optional[datetime] = Field(None, alias="repeatEndDate", serialization_alias="repeatEndDate")


class ScheduleCreate(ScheduleBase):
    """일정 생성 스키마"""

    reminders: List[ReminderCreate] = []


class ScheduleUpdate(BaseModel):
    """일정 수정 스키마"""
    model_config = ConfigDict(populate_by_name=True)

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    start_date: Optional[datetime] = Field(None, alias="startDate")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    all_day: Optional[bool] = Field(None, alias="allDay")
    priority: Optional[SchedulePriority] = None
    color: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=500)
    repeat: Optional[ScheduleRepeatType] = None
    repeat_end_date: Optional[datetime] = Field(None, alias="repeatEndDate")
    reminders: Optional[List[ReminderCreate]] = None


class ScheduleResponse(ScheduleBase):
    """일정 응답 스키마"""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    user_id: UUID = Field(..., alias="userId", serialization_alias="userId")
    image_url: Optional[str] = Field(None, alias="imageUrl", serialization_alias="imageUrl")
    reminders: List[ReminderResponse] = []
    created_at: datetime = Field(..., alias="createdAt", serialization_alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt", serialization_alias="updatedAt")


class ScheduleListResponse(BaseModel):
    """일정 목록 응답 스키마"""

    items: List[ScheduleResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ScheduleFilter(BaseModel):
    """일정 필터 스키마"""

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    priority: Optional[List[SchedulePriority]] = None
    search: Optional[str] = None

