# 🚀 AWS 배포 가이드

개인 프로젝트에 적합한 무료/저렴한 AWS 서비스를 활용한 배포 가이드입니다.

## 📋 목차

1. [비용 분석](#-비용-분석)
2. [사전 준비](#-사전-준비)
3. [옵션 A: EC2 단일 인스턴스 배포 (추천)](#-옵션-a-ec2-단일-인스턴스-배포-추천)
4. [옵션 B: CloudFormation 전체 인프라 배포](#-옵션-b-cloudformation-전체-인프라-배포)
5. [도메인 및 SSL 설정](#-도메인-및-ssl-설정)
6. [유지보수](#-유지보수)

---

## 💰 비용 분석

### AWS 프리 티어 (신규 계정 12개월)

| 서비스 | 무료 제공량 | 초과 시 비용 |
|--------|-------------|--------------|
| **EC2 t3.micro** | 750시간/월 | ~$8.5/월 |
| **RDS db.t3.micro** | 750시간/월 | ~$12/월 |
| **S3** | 5GB 저장소, 20,000 GET | 매우 저렴 |
| **EBS gp3** | 30GB/월 | $0.08/GB |
| **데이터 전송** | 100GB/월 | $0.09/GB |

### 배포 옵션별 예상 비용

#### 옵션 A: EC2 단일 인스턴스 (추천) 💡
```
EC2 t2.micro (무료) + EC2 내부 PostgreSQL & Redis + S3 (무료)
= 월 $0 (프리 티어) / 월 ~$10 (프리 티어 종료 후)
```

#### 옵션 B: CloudFormation 전체 인프라
```
EC2 + RDS + ElastiCache + S3
= 월 $0 (프리 티어) / 월 ~$30-50 (프리 티어 종료 후)
```

---

## 🔧 사전 준비

### 1. AWS 계정 생성

1. [AWS 홈페이지](https://aws.amazon.com/ko/) 접속
2. "무료로 시작하기" 클릭
3. 이메일, 비밀번호, 계정 이름 입력
4. 결제 정보 입력 (프리 티어 내에서는 청구되지 않음)

### 2. IAM 사용자 생성

> ⚠️ 루트 계정 대신 IAM 사용자를 사용하세요!

1. AWS 콘솔 → IAM → 사용자 → 사용자 생성
2. 사용자 이름: `ez-calendar-admin`
3. 권한 정책 연결:
   - `AmazonEC2FullAccess`
   - `AmazonS3FullAccess`
   - `AmazonRDSFullAccess` (옵션 B 선택 시)
4. 액세스 키 생성 (CLI 용)

### 3. AWS CLI 설치 및 설정

```bash
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Windows
# https://awscli.amazonaws.com/AWSCLIV2.msi 다운로드

# 설정
aws configure
```

입력 정보:
```
AWS Access Key ID: [IAM에서 발급받은 키]
AWS Secret Access Key: [IAM에서 발급받은 시크릿]
Default region name: ap-northeast-2
Default output format: json
```

### 4. EC2 키 페어 생성

```bash
aws ec2 create-key-pair \
    --key-name ez-calendar-key \
    --query 'KeyMaterial' \
    --output text > ~/.ssh/ez-calendar-key.pem

chmod 400 ~/.ssh/ez-calendar-key.pem
```

---

## 🖥️ 옵션 A: EC2 단일 인스턴스 배포 (추천)

> 모든 서비스를 EC2 하나에서 Docker로 실행하는 가장 저렴한 방식입니다.

### 방법 1: 자동화 스크립트 사용

```bash
cd infra/aws
chmod +x deploy-ec2.sh
./deploy-ec2.sh
```

### 방법 2: 수동 배포

#### Step 1: EC2 인스턴스 생성

**AWS 콘솔 사용:**
1. EC2 → 인스턴스 시작
2. 이름: `ez-calendar`
3. AMI: Amazon Linux 2023
4. 인스턴스 유형: **t3.micro** (프리 티어)
5. 키 페어: `ez-calendar-key`
6. 네트워크 설정:
   - 퍼블릭 IP 자동 할당: 활성화
   - 보안 그룹: 새로 생성
     - SSH (22): 내 IP
     - HTTP (80): 0.0.0.0/0
     - HTTPS (443): 0.0.0.0/0
7. 스토리지: **30GB** gp3 (프리 티어)
8. 인스턴스 시작

#### Step 2: EC2 접속 및 초기 설정

```bash
# EC2 접속
ssh -i ~/.ssh/ez-calendar-key.pem ec2-user@[EC2_PUBLIC_IP]

# 초기 설정 스크립트 실행
curl -sSL https://raw.githubusercontent.com/[YOUR_REPO]/main/infra/aws/setup-ec2.sh | bash

# 또는 수동으로:
sudo dnf update -y
sudo dnf install -y docker git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 재접속 (docker 그룹 적용)
exit
ssh -i ~/.ssh/ez-calendar-key.pem ec2-user@[EC2_PUBLIC_IP]

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Step 3: 프로젝트 배포

```bash
# 프로젝트 클론
git clone [YOUR_REPOSITORY_URL] ~/ez-calendar
cd ~/ez-calendar

# 환경 변수 설정
cp env.production.example .env
nano .env  # 실제 값으로 수정
```

**.env 파일 예시:**
```bash
DB_PASSWORD=YourSecurePassword123!
SECRET_KEY=$(openssl rand -hex 32)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=ap-northeast-2
AWS_S3_BUCKET=ez-calendar-uploads-123456789012
```

```bash
# 애플리케이션 실행
docker-compose -f docker-compose.ec2.yml up -d --build

# 상태 확인
docker-compose -f docker-compose.ec2.yml ps

# 로그 확인
docker-compose -f docker-compose.ec2.yml logs -f
```

#### Step 4: 데이터베이스 마이그레이션

```bash
# 백엔드 컨테이너에서 마이그레이션 실행
docker-compose -f docker-compose.ec2.yml exec backend alembic upgrade head
```

#### Step 5: S3 버킷 생성

```bash
# AWS 계정 ID 확인
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

# S3 버킷 생성
aws s3api create-bucket \
    --bucket ez-calendar-uploads-${ACCOUNT_ID} \
    --region ap-northeast-2 \
    --create-bucket-configuration LocationConstraint=ap-northeast-2

# 퍼블릭 액세스 차단
aws s3api put-public-access-block \
    --bucket ez-calendar-uploads-${ACCOUNT_ID} \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

#### Step 6: 접속 확인

브라우저에서 `http://[EC2_PUBLIC_IP]` 접속

---

## 🏗️ 옵션 B: CloudFormation 전체 인프라 배포

> RDS, ElastiCache 등 AWS 관리형 서비스를 사용하는 방식입니다.
> 프리 티어 종료 후 비용이 더 발생하지만, 더 안정적입니다.

### 배포 실행

```bash
cd infra/aws
chmod +x deploy.sh

# 환경 변수 설정
export DB_PASSWORD="YourSecurePassword123!"
export EC2_KEY_PAIR="ez-calendar-key"

# 배포 실행
./deploy.sh dev
```

### 배포 후 EC2 설정

배포 완료 후 출력되는 EC2 IP로 접속:

```bash
ssh -i ~/.ssh/ez-calendar-key.pem ec2-user@[EC2_PUBLIC_IP]

# Docker 설정
# ... (위 Step 2와 동일)

# 환경 변수에 RDS 엔드포인트 추가
cat >> .env << EOF
DATABASE_URL=postgresql+asyncpg://postgres:${DB_PASSWORD}@[RDS_ENDPOINT]:5432/ez_calendar
EOF
```

---

## 🌐 도메인 및 SSL 설정

### 1. 도메인 구매 (선택사항)

- **Route 53**: AWS에서 도메인 구매 (~$12/년 for .com)
- **외부 도메인**: Namecheap, GoDaddy 등

### 2. Elastic IP 할당

EC2 인스턴스에 고정 IP 할당:

```bash
# Elastic IP 할당
aws ec2 allocate-address --domain vpc

# EC2에 연결
aws ec2 associate-address \
    --instance-id [INSTANCE_ID] \
    --allocation-id [ALLOCATION_ID]
```

### 3. Route 53 설정 (AWS 도메인 사용 시)

1. Route 53 → 호스팅 영역 생성
2. A 레코드 추가: `@` → EC2 Elastic IP
3. CNAME 레코드: `www` → `@`

### 4. Let's Encrypt SSL 인증서

```bash
# EC2에서 실행
sudo dnf install -y certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# 인증서 자동 갱신 설정
echo "0 12 * * * root certbot renew --quiet" | sudo tee -a /etc/crontab
```

### 5. Nginx SSL 설정

`infra/nginx/nginx.conf` 수정:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... 나머지 설정
}
```

---

## 🔄 유지보수

### 애플리케이션 업데이트

```bash
cd ~/ez-calendar
git pull origin main
docker-compose -f docker-compose.ec2.yml up -d --build
```

### 로그 확인

```bash
# 전체 로그
docker-compose -f docker-compose.ec2.yml logs -f

# 특정 서비스 로그
docker-compose -f docker-compose.ec2.yml logs -f backend
```

### 데이터베이스 백업

```bash
# PostgreSQL 백업
docker-compose -f docker-compose.ec2.yml exec postgres pg_dump -U postgres ez_calendar > backup_$(date +%Y%m%d).sql

# S3에 백업 업로드
aws s3 cp backup_$(date +%Y%m%d).sql s3://ez-calendar-uploads-[ACCOUNT_ID]/backups/
```

### 서비스 재시작

```bash
docker-compose -f docker-compose.ec2.yml restart
```

### 리소스 모니터링

```bash
# Docker 리소스 사용량
docker stats

# 디스크 사용량
df -h

# 메모리 사용량
free -m
```

---

## 🚨 문제 해결

### Docker 권한 오류
```bash
# docker 그룹에 사용자 추가 후 재접속
sudo usermod -aG docker $USER
exit
# 다시 SSH 접속
```

### 포트 80 이미 사용 중
```bash
# 사용 중인 프로세스 확인
sudo lsof -i :80
sudo kill -9 [PID]
```

### 메모리 부족 (t2.micro)
```bash
# 스왑 파일 생성
sudo dd if=/dev/zero of=/swapfile bs=128M count=16
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```

### 데이터베이스 연결 실패
```bash
# PostgreSQL 컨테이너 상태 확인
docker-compose -f docker-compose.ec2.yml logs postgres

# 컨테이너 재시작
docker-compose -f docker-compose.ec2.yml restart postgres
```

---

## 📚 참고 자료

- [AWS 프리 티어 FAQ](https://aws.amazon.com/ko/free/free-tier-faqs/)
- [EC2 인스턴스 유형](https://aws.amazon.com/ko/ec2/instance-types/)
- [Docker Compose 문서](https://docs.docker.com/compose/)
- [Let's Encrypt 문서](https://letsencrypt.org/docs/)
