from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.schedule import SchedulePriority
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
    ScheduleListResponse,
)
from app.schemas.common import MessageResponse
from app.services.schedule_service import ScheduleService
from app.services.file_service import FileService

router = APIRouter()


@router.get("")
async def get_schedules(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_date: Optional[datetime] = Query(None, alias="startDate"),
    end_date: Optional[datetime] = Query(None, alias="endDate"),
    priority: Optional[List[SchedulePriority]] = Query(None),
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """일정 목록 조회"""
    schedule_service = ScheduleService(db)
    schedules, total = await schedule_service.get_list(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        start_date=start_date,
        end_date=end_date,
        priority=priority,
        search=search,
    )

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": [ScheduleResponse.model_validate(s).model_dump(by_alias=True) for s in schedules],
        "total": total,
        "page": page,
        "pageSize": page_size,
        "totalPages": total_pages,
    }


@router.get("/range")
async def get_schedules_by_range(
    start_date: datetime = Query(..., alias="startDate"),
    end_date: datetime = Query(..., alias="endDate"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """날짜 범위로 일정 조회"""
    schedule_service = ScheduleService(db)
    schedules = await schedule_service.get_by_date_range(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "data": [ScheduleResponse.model_validate(s).model_dump(by_alias=True) for s in schedules],
    }


@router.get("/{schedule_id}")
async def get_schedule(
    schedule_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """일정 상세 조회"""
    schedule_service = ScheduleService(db)
    schedule = await schedule_service.get_by_id(schedule_id, current_user.id)

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일정을 찾을 수 없습니다.",
        )

    return {"data": ScheduleResponse.model_validate(schedule).model_dump(by_alias=True)}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_in: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """일정 생성"""
    schedule_service = ScheduleService(db)
    schedule = await schedule_service.create(current_user.id, schedule_in)
    return {"data": ScheduleResponse.model_validate(schedule).model_dump(by_alias=True)}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def create_schedule_with_image(
    title: str = Form(...),
    startDate: str = Form(...),
    image: UploadFile = File(...),
    endDate: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    allDay: str = Form("false"),
    priority: str = Form("default"),
    color: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """이미지와 함께 일정 생성"""
    from dateutil.parser import parse as parse_date
    
    # Form 데이터 파싱
    start_date_parsed = parse_date(startDate)
    end_date_parsed = parse_date(endDate) if endDate and endDate.strip() else None
    all_day_parsed = allDay.lower() in ("true", "1", "yes")
    priority_parsed = SchedulePriority(priority) if priority else SchedulePriority.DEFAULT
    
    # 빈 문자열을 None으로 변환
    description_clean = description if description and description.strip() else None
    color_clean = color if color and color.strip() else None
    location_clean = location if location and location.strip() else None
    
    # 이미지 업로드
    file_service = FileService()
    image_url = await file_service.upload_image(image, current_user.id)

    # 일정 생성
    schedule_in = ScheduleCreate(
        title=title,
        description=description_clean,
        start_date=start_date_parsed,
        end_date=end_date_parsed,
        all_day=all_day_parsed,
        priority=priority_parsed,
        color=color_clean,
        location=location_clean,
    )

    schedule_service = ScheduleService(db)
    schedule = await schedule_service.create(current_user.id, schedule_in, image_url=image_url)

    return {"data": ScheduleResponse.model_validate(schedule).model_dump(by_alias=True)}


@router.put("/{schedule_id}")
async def update_schedule(
    schedule_id: UUID,
    schedule_in: ScheduleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """일정 수정"""
    schedule_service = ScheduleService(db)

    # 일정 존재 및 권한 확인
    schedule = await schedule_service.get_by_id(schedule_id, current_user.id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일정을 찾을 수 없습니다.",
        )

    updated_schedule = await schedule_service.update(schedule_id, schedule_in)
    return {"data": ScheduleResponse.model_validate(updated_schedule).model_dump(by_alias=True)}


@router.delete("/{schedule_id}", response_model=MessageResponse)
async def delete_schedule(
    schedule_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """일정 삭제"""
    schedule_service = ScheduleService(db)

    # 일정 존재 및 권한 확인
    schedule = await schedule_service.get_by_id(schedule_id, current_user.id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일정을 찾을 수 없습니다.",
        )

    # 이미지 삭제
    if schedule.image_url:
        file_service = FileService()
        await file_service.delete_image(schedule.image_url)

    await schedule_service.delete(schedule_id)
    return MessageResponse(message="일정이 삭제되었습니다.")

