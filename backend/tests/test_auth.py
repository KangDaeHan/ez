import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """헬스체크 테스트"""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == settings.VERSION


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """회원가입 테스트"""
    user_data = {
        "email": "test@example.com",
        "name": "테스트 사용자",
        "password": "testpassword123",
    }
    response = await client.post(f"{settings.API_V1_PREFIX}/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """중복 이메일 회원가입 테스트"""
    user_data = {
        "email": "duplicate@example.com",
        "name": "테스트 사용자",
        "password": "testpassword123",
    }
    # 첫 번째 가입
    await client.post(f"{settings.API_V1_PREFIX}/auth/register", json=user_data)

    # 중복 가입 시도
    response = await client.post(f"{settings.API_V1_PREFIX}/auth/register", json=user_data)
    assert response.status_code == 400
    assert "이미 등록된 이메일" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """로그인 성공 테스트"""
    # 회원가입
    user_data = {
        "email": "login@example.com",
        "name": "테스트 사용자",
        "password": "testpassword123",
    }
    await client.post(f"{settings.API_V1_PREFIX}/auth/register", json=user_data)

    # 로그인
    login_data = {"email": user_data["email"], "password": user_data["password"]}
    response = await client.post(f"{settings.API_V1_PREFIX}/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """잘못된 비밀번호 로그인 테스트"""
    # 회원가입
    user_data = {
        "email": "wrongpw@example.com",
        "name": "테스트 사용자",
        "password": "testpassword123",
    }
    await client.post(f"{settings.API_V1_PREFIX}/auth/register", json=user_data)

    # 잘못된 비밀번호로 로그인
    login_data = {"email": user_data["email"], "password": "wrongpassword"}
    response = await client.post(f"{settings.API_V1_PREFIX}/auth/login", json=login_data)
    assert response.status_code == 401

