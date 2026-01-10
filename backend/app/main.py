from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 라이프사이클 관리"""
    # Startup
    print("🚀 Starting up EZ Calendar API...")
    
    # 개발 환경에서 uploads 폴더 생성
    if settings.DEBUG:
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        print("📁 Uploads directory ready!")
    
    yield
    # Shutdown
    print("👋 Shutting down EZ Calendar API...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="위젯형 일정관리 달력 API",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# 개발 환경에서 정적 파일 서빙 (이미지 업로드)
if settings.DEBUG:
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "version": settings.VERSION}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )

