import pytest
from datetime import datetime
from httpx import AsyncClient

from app.core.config import settings


async def get_auth_header(client: AsyncClient, email: str = "schedule@example.com") -> dict:
    """인증 헤더 생성 헬퍼"""
    user_data = {
        "email": email,
        "name": "테스트 사용자",
        "password": "testpassword123",
    }
    await client.post(f"{settings.API_V1_PREFIX}/auth/register", json=user_data)

    login_data = {"email": email, "password": "testpassword123"}
    response = await client.post(f"{settings.API_V1_PREFIX}/auth/login", json=login_data)
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_schedule(client: AsyncClient):
    """일정 생성 테스트"""
    headers = await get_auth_header(client, "create@example.com")

    schedule_data = {
        "title": "테스트 일정",
        "description": "테스트 설명",
        "start_date": datetime.now().isoformat(),
        "all_day": False,
        "priority": "default",
        "repeat": "none",
        "reminders": [],
    }

    response = await client.post(
        f"{settings.API_V1_PREFIX}/schedules", json=schedule_data, headers=headers
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["title"] == schedule_data["title"]
    assert data["description"] == schedule_data["description"]


@pytest.mark.asyncio
async def test_get_schedules(client: AsyncClient):
    """일정 목록 조회 테스트"""
    headers = await get_auth_header(client, "list@example.com")

    # 일정 생성
    schedule_data = {
        "title": "목록 테스트 일정",
        "start_date": datetime.now().isoformat(),
        "all_day": False,
        "priority": "high",
        "repeat": "none",
        "reminders": [],
    }
    await client.post(f"{settings.API_V1_PREFIX}/schedules", json=schedule_data, headers=headers)

    # 목록 조회
    response = await client.get(f"{settings.API_V1_PREFIX}/schedules", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_schedule_by_id(client: AsyncClient):
    """일정 상세 조회 테스트"""
    headers = await get_auth_header(client, "detail@example.com")

    # 일정 생성
    schedule_data = {
        "title": "상세 테스트 일정",
        "start_date": datetime.now().isoformat(),
        "all_day": True,
        "priority": "medium",
        "repeat": "none",
        "reminders": [],
    }
    create_response = await client.post(
        f"{settings.API_V1_PREFIX}/schedules", json=schedule_data, headers=headers
    )
    schedule_id = create_response.json()["data"]["id"]

    # 상세 조회
    response = await client.get(
        f"{settings.API_V1_PREFIX}/schedules/{schedule_id}", headers=headers
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == schedule_data["title"]


@pytest.mark.asyncio
async def test_update_schedule(client: AsyncClient):
    """일정 수정 테스트"""
    headers = await get_auth_header(client, "update@example.com")

    # 일정 생성
    schedule_data = {
        "title": "수정 전 일정",
        "start_date": datetime.now().isoformat(),
        "all_day": False,
        "priority": "low",
        "repeat": "none",
        "reminders": [],
    }
    create_response = await client.post(
        f"{settings.API_V1_PREFIX}/schedules", json=schedule_data, headers=headers
    )
    schedule_id = create_response.json()["data"]["id"]

    # 수정
    update_data = {"title": "수정 후 일정", "priority": "high"}
    response = await client.put(
        f"{settings.API_V1_PREFIX}/schedules/{schedule_id}", json=update_data, headers=headers
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == update_data["title"]
    assert data["priority"] == update_data["priority"]


@pytest.mark.asyncio
async def test_delete_schedule(client: AsyncClient):
    """일정 삭제 테스트"""
    headers = await get_auth_header(client, "delete@example.com")

    # 일정 생성
    schedule_data = {
        "title": "삭제할 일정",
        "start_date": datetime.now().isoformat(),
        "all_day": False,
        "priority": "default",
        "repeat": "none",
        "reminders": [],
    }
    create_response = await client.post(
        f"{settings.API_V1_PREFIX}/schedules", json=schedule_data, headers=headers
    )
    schedule_id = create_response.json()["data"]["id"]

    # 삭제
    response = await client.delete(
        f"{settings.API_V1_PREFIX}/schedules/{schedule_id}", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

    # 삭제 확인
    get_response = await client.get(
        f"{settings.API_V1_PREFIX}/schedules/{schedule_id}", headers=headers
    )
    assert get_response.status_code == 404

