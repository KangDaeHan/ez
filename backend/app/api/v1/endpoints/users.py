from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import MessageResponse
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """현재 사용자 정보 조회"""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """현재 사용자 정보 수정"""
    user_service = UserService(db)
    updated_user = await user_service.update(current_user.id, user_in)
    return UserResponse.model_validate(updated_user)


@router.delete("/me", response_model=MessageResponse)
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """현재 사용자 계정 삭제"""
    user_service = UserService(db)
    await user_service.delete(current_user.id)
    return MessageResponse(message="계정이 삭제되었습니다.")

