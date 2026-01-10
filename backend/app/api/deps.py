from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.core.security import decode_token, get_password_hash
from app.models.user import User
from app.services.user_service import UserService

security = HTTPBearer(auto_error=False)  # 개발 모드에서 인증 선택적으로 처리

# 개발용 테스트 사용자 ID
DEV_USER_EMAIL = "dev@test.com"
DEV_USER_NAME = "개발 테스트 사용자"


async def get_or_create_dev_user(db: AsyncSession) -> User:
    """개발용 테스트 사용자 조회 또는 생성"""
    user_service = UserService(db)
    user = await user_service.get_by_email(DEV_USER_EMAIL)
    
    if not user:
        # 개발용 사용자 생성
        user = User(
            email=DEV_USER_EMAIL,
            name=DEV_USER_NAME,
            hashed_password=get_password_hash("devpassword123"),
            is_active=True,
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
    
    return user


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """현재 로그인한 사용자 조회"""
    
    # 개발 모드이고 토큰이 없으면 개발용 사용자 반환
    if settings.DEBUG and not credentials:
        return await get_or_create_dev_user(db)
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials

    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="액세스 토큰이 아닙니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service = UserService(db)
    user = await user_service.get_by_id(payload["sub"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다.",
        )

    return user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """현재 관리자 사용자 조회"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )
    return current_user

