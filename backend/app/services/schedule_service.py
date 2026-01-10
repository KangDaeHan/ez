from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.schedule import Schedule, ScheduleReminder, SchedulePriority
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate


class ScheduleService:
    """일정 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, schedule_id: UUID, user_id: UUID) -> Optional[Schedule]:
        """ID로 일정 조회"""
        result = await self.db.execute(
            select(Schedule)
            .options(selectinload(Schedule.reminders))
            .where(and_(Schedule.id == schedule_id, Schedule.user_id == user_id))
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        priority: Optional[List[SchedulePriority]] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Schedule], int]:
        """일정 목록 조회 (페이지네이션)"""
        # 기본 쿼리
        query = select(Schedule).options(selectinload(Schedule.reminders)).where(
            Schedule.user_id == user_id
        )

        # 날짜 필터
        if start_date:
            query = query.where(Schedule.start_date >= start_date)
        if end_date:
            query = query.where(Schedule.start_date <= end_date)

        # 우선순위 필터
        if priority:
            query = query.where(Schedule.priority.in_(priority))

        # 검색
        if search:
            search_filter = or_(
                Schedule.title.ilike(f"%{search}%"),
                Schedule.description.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)

        # 전체 개수 조회
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # 페이지네이션 및 정렬
        query = query.order_by(Schedule.start_date.asc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        schedules = list(result.scalars().all())

        return schedules, total

    async def get_by_date_range(
        self,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Schedule]:
        """날짜 범위로 일정 조회"""
        result = await self.db.execute(
            select(Schedule)
            .options(selectinload(Schedule.reminders))
            .where(
                and_(
                    Schedule.user_id == user_id,
                    Schedule.start_date >= start_date,
                    Schedule.start_date <= end_date,
                )
            )
            .order_by(Schedule.start_date.asc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        user_id: UUID,
        schedule_in: ScheduleCreate,
        image_url: Optional[str] = None,
    ) -> Schedule:
        """일정 생성"""
        schedule_data = schedule_in.model_dump(exclude={"reminders"})
        schedule = Schedule(user_id=user_id, image_url=image_url, **schedule_data)

        # 알림 생성
        for reminder_in in schedule_in.reminders:
            reminder = ScheduleReminder(
                reminder_type=reminder_in.reminder_type,
                minutes_before=reminder_in.minutes_before,
            )
            schedule.reminders.append(reminder)

        self.db.add(schedule)
        await self.db.flush()
        
        # 관계를 포함하여 다시 조회
        result = await self.db.execute(
            select(Schedule)
            .options(selectinload(Schedule.reminders))
            .where(Schedule.id == schedule.id)
        )
        return result.scalar_one()

    async def update(self, schedule_id: UUID, schedule_in: ScheduleUpdate) -> Optional[Schedule]:
        """일정 수정"""
        result = await self.db.execute(
            select(Schedule)
            .options(selectinload(Schedule.reminders))
            .where(Schedule.id == schedule_id)
        )
        schedule = result.scalar_one_or_none()

        if not schedule:
            return None

        update_data = schedule_in.model_dump(exclude_unset=True, exclude={"reminders"})
        for field, value in update_data.items():
            setattr(schedule, field, value)

        # 알림 업데이트
        if schedule_in.reminders is not None:
            # 기존 알림 삭제
            for reminder in schedule.reminders:
                await self.db.delete(reminder)

            # 새 알림 생성
            for reminder_in in schedule_in.reminders:
                reminder = ScheduleReminder(
                    schedule_id=schedule_id,
                    reminder_type=reminder_in.reminder_type,
                    minutes_before=reminder_in.minutes_before,
                )
                self.db.add(reminder)

        await self.db.flush()
        
        # 관계를 포함하여 다시 조회
        result = await self.db.execute(
            select(Schedule)
            .options(selectinload(Schedule.reminders))
            .where(Schedule.id == schedule_id)
        )
        return result.scalar_one()

    async def delete(self, schedule_id: UUID) -> bool:
        """일정 삭제"""
        result = await self.db.execute(
            select(Schedule).where(Schedule.id == schedule_id)
        )
        schedule = result.scalar_one_or_none()

        if not schedule:
            return False

        await self.db.delete(schedule)
        await self.db.flush()
        return True

