from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """사용자 기본 스키마"""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """사용자 생성 스키마"""

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """사용자 수정 스키마"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """사용자 응답 스키마"""

    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """로그인 요청 스키마"""

    email: EmailStr
    password: str


class Token(BaseModel):
    """토큰 응답 스키마"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """토큰 페이로드 스키마"""

    sub: str
    exp: int
    type: str

