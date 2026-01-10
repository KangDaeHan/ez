from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, schedules, system

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["인증"])
api_router.include_router(users.router, prefix="/users", tags=["사용자"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["일정"])
api_router.include_router(system.router, prefix="/system", tags=["시스템"])

