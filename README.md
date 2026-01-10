# 📅 EZ Calendar - 위젯형 일정관리 달력

내 맘대로 꾸미는 위젯형 일정관리 달력 애플리케이션입니다.

## 🚀 기술 스택

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **Language**: TypeScript
- **State Management**: Pinia
- **Data Fetching**: TanStack Query (Vue Query)
- **Build Tool**: Vite
- **Package Manager**: pnpm
- **Styling**: Tailwind CSS
- **Testing**: Vitest + Vue Test Utils

### Backend
- **Framework**: FastAPI (Python)
- **Runtime**: Python 3.11+
- **ORM**: SQLAlchemy
- **Migration**: Alembic

### Database
- **Primary DB**: PostgreSQL
- **Cache**: Redis

### Infrastructure
- **Cloud**: AWS (EC2 Free Tier)
- **Container**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## 📁 프로젝트 구조

```
ez/
├── frontend/                 # Vue.js 프론트엔드 (FSD 구조)
│   ├── src/
│   │   ├── app/             # 앱 초기화, 프로바이더, 스타일
│   │   ├── processes/       # 페이지 간 프로세스
│   │   ├── pages/           # 페이지 컴포넌트
│   │   ├── widgets/         # 독립적인 UI 블록
│   │   ├── features/        # 비즈니스 기능
│   │   ├── entities/        # 비즈니스 엔티티
│   │   └── shared/          # 공유 유틸리티, UI
│   ├── tests/               # 테스트 파일
│   └── ...
├── backend/                  # FastAPI 백엔드
│   ├── app/
│   │   ├── api/             # API 라우터
│   │   ├── core/            # 핵심 설정
│   │   ├── models/          # DB 모델
│   │   ├── schemas/         # Pydantic 스키마
│   │   ├── services/        # 비즈니스 로직
│   │   └── utils/           # 유틸리티
│   ├── migrations/          # Alembic 마이그레이션
│   └── tests/               # 테스트 파일
├── infra/                   # 인프라 설정
│   ├── docker/              # Docker 설정
│   ├── aws/                 # AWS 설정
│   └── nginx/               # Nginx 설정
└── docs/                    # 문서
```

## 🛠️ 설치 및 실행

### 요구사항
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- pnpm 8+

### Frontend 설정

```bash
cd frontend
pnpm install
pnpm dev
```

### Backend 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker로 전체 실행

```bash
docker-compose up -d
```

## 🔧 환경 설정

### 개발 환경
- Frontend: `frontend/.env.development`
- Backend: `backend/.env.development`

### 운영 환경
- Frontend: `frontend/.env.production`
- Backend: `backend/.env.production`

## 📱 주요 기능

### 달력 기능
- ✅ 월별/주별/일별 보기
- ✅ 한국 공휴일 표시
- ✅ 음력 날짜 표시
- ✅ 위젯 커스터마이징

### 일정 관리
- ✅ 일정 등록/수정/삭제
- ✅ 이미지 첨부
- ✅ 반복 일정
- ✅ 알림 설정

### 위젯
- ✅ 맥 바탕화면 위젯 (Electron)
- ✅ 다양한 위젯 크기
- ✅ 테마 커스터마이징

## 📚 API 문서

서버 실행 후 아래 URL에서 확인 가능합니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 테스트

### Frontend
```bash
cd frontend
pnpm test        # 단위 테스트
pnpm test:e2e    # E2E 테스트
```

### Backend
```bash
cd backend
pytest
```

## 📄 라이선스

MIT License

