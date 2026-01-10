#!/bin/bash

# ============================================
# EC2 자동 설정 배포 스크립트
# User Data로 Docker 자동 설치
# EC2 Instance Connect로 접속
# ============================================

set -e

AWS_REGION=${AWS_REGION:-ap-northeast-2}
INSTANCE_TYPE=${INSTANCE_TYPE:-t3.micro}
AMI_ID=${AMI_ID:-ami-0c9c942bd7bf113a2}

echo ""
echo "=========================================="
echo "🚀 EC2 자동 설정 배포"
echo "=========================================="
echo ""

# 1. 기존 인스턴스 정리
echo "🗑️ 기존 인스턴스 정리 중..."
for id in $(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=ez-calendar" "Name=instance-state-name,Values=running,stopped,pending" \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text \
    --region $AWS_REGION 2>/dev/null); do
    aws ec2 terminate-instances --instance-ids $id --region $AWS_REGION 2>/dev/null || true
done

sleep 30

# 2. VPC 및 서브넷 확인
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text --region $AWS_REGION)
SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[0].SubnetId' --output text --region $AWS_REGION)

# 3. 보안 그룹 확인/생성
SG_ID=$(aws ec2 describe-security-groups --filters "Name=group-name,Values=ez-calendar-sg" "Name=vpc-id,Values=$VPC_ID" --query 'SecurityGroups[0].GroupId' --output text --region $AWS_REGION 2>/dev/null)

if [ "$SG_ID" == "None" ] || [ -z "$SG_ID" ]; then
    echo "🔒 보안 그룹 생성 중..."
    SG_ID=$(aws ec2 create-security-group --group-name ez-calendar-sg --description "EZ Calendar SG" --vpc-id $VPC_ID --query 'GroupId' --output text --region $AWS_REGION)
    aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 --region $AWS_REGION
    aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0 --region $AWS_REGION
    aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 443 --cidr 0.0.0.0/0 --region $AWS_REGION
fi

# 4. User Data 스크립트 (자동 설정)
USER_DATA=$(cat << 'USERDATA'
#!/bin/bash
exec > /var/log/user-data.log 2>&1
set -x

# Docker 설치
dnf update -y
dnf install -y docker git

# Docker 서비스 시작
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

# Docker Compose 설치
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 완료 표시
touch /home/ec2-user/SETUP_COMPLETE
chown ec2-user:ec2-user /home/ec2-user/SETUP_COMPLETE

echo "=== Setup Complete ==="
USERDATA
)

# 5. EC2 인스턴스 생성 (키 페어 없이!)
echo "🖥️ EC2 인스턴스 생성 중..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type $INSTANCE_TYPE \
    --security-group-ids $SG_ID \
    --subnet-id $SUBNET_ID \
    --associate-public-ip-address \
    --iam-instance-profile Name=EC2InstanceConnect 2>/dev/null || \
aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type $INSTANCE_TYPE \
    --security-group-ids $SG_ID \
    --subnet-id $SUBNET_ID \
    --associate-public-ip-address \
    --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":30,"VolumeType":"gp3"}}]' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ez-calendar}]' \
    --user-data "$USER_DATA" \
    --query 'Instances[0].InstanceId' \
    --output text \
    --region $AWS_REGION)

echo "⏳ 인스턴스 시작 대기 중..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $AWS_REGION

# 6. Public IP 가져오기
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text --region $AWS_REGION)

# 7. S3 버킷 생성
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
S3_BUCKET="ez-calendar-uploads-${ACCOUNT_ID}"
aws s3api create-bucket --bucket $S3_BUCKET --region $AWS_REGION --create-bucket-configuration LocationConstraint=$AWS_REGION 2>/dev/null || true

echo ""
echo "=========================================="
echo "✅ 배포 완료!"
echo "=========================================="
echo ""
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo "S3 Bucket: $S3_BUCKET"
echo ""
echo "=========================================="
echo "📋 다음 단계"
echo "=========================================="
echo ""
echo "1. AWS 콘솔에서 EC2 Instance Connect로 접속:"
echo "   - AWS 콘솔 → EC2 → 인스턴스 → $INSTANCE_ID 선택"
echo "   - '연결' 버튼 클릭 → 'EC2 Instance Connect' 탭 → '연결'"
echo ""
echo "2. 설정 완료 확인 (약 2-3분 후):"
echo "   ls /home/ec2-user/SETUP_COMPLETE"
echo ""
echo "3. Docker 확인:"
echo "   docker --version"
echo "   docker-compose --version"
echo ""
echo "4. 프로젝트 배포:"
echo "   git clone [YOUR_REPO] ~/ez-calendar"
echo "   cd ~/ez-calendar"
echo "   # .env 파일 생성"
echo "   docker-compose -f docker-compose.ec2.yml up -d --build"
echo ""
echo "=========================================="
echo "🌐 웹 접속: http://$PUBLIC_IP"
echo "=========================================="
