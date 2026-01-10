#!/bin/bash

# ============================================
# EC2 인스턴스 초기 설정 스크립트
# EC2에 SSH 접속 후 실행
# Amazon Linux 2023 용 (dnf 사용)
# ============================================

set -e

echo "🔧 EC2 인스턴스 초기 설정 시작..."

# 1. 시스템 업데이트
echo "📦 시스템 업데이트 중..."
sudo dnf update -y

# 2. Docker 설치
echo "🐳 Docker 설치 중..."
sudo dnf install -y docker git

# 3. Docker 서비스 시작 및 활성화
echo "🚀 Docker 서비스 시작..."
sudo systemctl start docker
sudo systemctl enable docker

# 4. 현재 사용자를 docker 그룹에 추가
echo "👤 Docker 그룹 설정..."
sudo usermod -aG docker $USER

# 5. Docker Compose 설치
echo "📥 Docker Compose 설치 중..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 6. Docker Compose 버전 확인
echo "✅ 설치 확인..."
docker --version
docker-compose --version

echo ""
echo "=========================================="
echo "✅ EC2 초기 설정 완료!"
echo "=========================================="
echo ""
echo "⚠️  중요: Docker 그룹 변경을 적용하려면"
echo "   세션을 종료하고 다시 접속하세요:"
echo ""
echo "   exit"
echo "   ssh -i ~/.ssh/ez-calendar-key.pem ec2-user@[PUBLIC_IP]"
echo ""
