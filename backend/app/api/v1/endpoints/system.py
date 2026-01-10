from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()


@router.get("/time")
async def get_server_time() -> dict:
    """서버 현재 시간 조회 (UTC 기준)"""
    now = datetime.now(timezone.utc)
    return {
        "serverTime": now.isoformat(),
        "timestamp": int(now.timestamp() * 1000),  # 밀리초 단위
    }


@router.get("/health")
async def health_check() -> dict:
    """서버 상태 확인"""
    return {
        "status": "ok",
        "serverTime": datetime.now(timezone.utc).isoformat(),
    }
