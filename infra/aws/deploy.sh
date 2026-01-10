#!/bin/bash

# EZ Calendar AWS Deployment Script
# This script deploys the application to AWS EC2

set -e

# Configuration
ENVIRONMENT=${1:-dev}
AWS_REGION=${AWS_REGION:-ap-northeast-2}
STACK_NAME="ez-calendar-${ENVIRONMENT}"
EC2_KEY_PAIR=${EC2_KEY_PAIR:-ez-calendar-key}
DB_PASSWORD=${DB_PASSWORD:-}

echo "🚀 Deploying EZ Calendar to AWS (${ENVIRONMENT} environment)"

# Check required environment variables
if [ -z "$DB_PASSWORD" ]; then
    echo "❌ Error: DB_PASSWORD environment variable is required"
    exit 1
fi

# Deploy CloudFormation stack
echo "📦 Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file cloudformation.yaml \
    --stack-name ${STACK_NAME} \
    --parameter-overrides \
        Environment=${ENVIRONMENT} \
        EC2KeyPair=${EC2_KEY_PAIR} \
        DBPassword=${DB_PASSWORD} \
    --capabilities CAPABILITY_IAM \
    --region ${AWS_REGION}

# Get outputs
echo "📋 Getting stack outputs..."
EC2_IP=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --query 'Stacks[0].Outputs[?OutputKey==`EC2PublicIP`].OutputValue' \
    --output text \
    --region ${AWS_REGION})

RDS_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --query 'Stacks[0].Outputs[?OutputKey==`RDSEndpoint`].OutputValue' \
    --output text \
    --region ${AWS_REGION})

S3_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
    --output text \
    --region ${AWS_REGION})

echo ""
echo "✅ Deployment Complete!"
echo "================================"
echo "EC2 Public IP: ${EC2_IP}"
echo "RDS Endpoint: ${RDS_ENDPOINT}"
echo "S3 Bucket: ${S3_BUCKET}"
echo "================================"
echo ""
echo "Next steps:"
echo "1. SSH into EC2: ssh -i ~/.ssh/${EC2_KEY_PAIR}.pem ec2-user@${EC2_IP}"
echo "2. Clone the repository and set up environment variables"
echo "3. Run docker-compose -f docker-compose.prod.yml up -d"

