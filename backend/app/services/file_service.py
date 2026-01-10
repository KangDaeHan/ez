import os
import uuid
from io import BytesIO
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException, status
from PIL import Image

from app.core.config import settings


class FileService:
    """파일 업로드 서비스 (개발: 로컬, 운영: AWS S3)"""

    def __init__(self):
        self.is_dev = settings.DEBUG
        
        if not self.is_dev:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            )
            self.bucket = settings.AWS_S3_BUCKET
        else:
            # 개발 환경: 로컬 uploads 폴더 사용
            self.upload_dir = Path("uploads")
            self.upload_dir.mkdir(exist_ok=True)

    def _validate_image(self, file: UploadFile) -> None:
        """이미지 유효성 검사"""
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"허용되지 않는 파일 형식입니다. 허용: {', '.join(settings.ALLOWED_IMAGE_TYPES)}",
            )

    def _generate_filename(self, user_id: uuid.UUID, filename: str) -> str:
        """파일명 생성"""
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
        unique_id = uuid.uuid4().hex[:8]
        return f"{user_id}_{unique_id}.{ext}"

    def _generate_key(self, user_id: uuid.UUID, filename: str) -> str:
        """S3 키 생성"""
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
        unique_id = uuid.uuid4().hex[:8]
        return f"schedules/{user_id}/{unique_id}.{ext}"

    async def _optimize_image(self, contents: bytes, file: UploadFile) -> bytes:
        """이미지 최적화"""
        try:
            img = Image.open(BytesIO(contents))
            # EXIF 회전 보정
            if hasattr(img, "_getexif") and img._getexif():
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)

            # 리사이즈 (최대 1920px)
            max_size = (1920, 1920)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # 최적화된 이미지를 바이트로 변환
            buffer = BytesIO()
            img_format = "JPEG" if img.mode == "RGB" else "PNG"
            img.save(buffer, format=img_format, quality=85, optimize=True)
            return buffer.getvalue()
        except Exception:
            # 이미지 처리 실패 시 원본 반환
            return contents

    async def upload_image(self, file: UploadFile, user_id: uuid.UUID) -> str:
        """이미지 업로드"""
        self._validate_image(file)

        # 파일 크기 확인
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"파일 크기는 {settings.MAX_FILE_SIZE // (1024 * 1024)}MB 이하여야 합니다.",
            )

        # 이미지 최적화
        contents = await self._optimize_image(contents, file)

        if self.is_dev:
            # 개발 환경: 로컬 파일 시스템에 저장
            return await self._upload_local(contents, user_id, file.filename or "image.jpg")
        else:
            # 운영 환경: S3에 업로드
            return await self._upload_s3(contents, user_id, file.filename or "image.jpg", file.content_type)

    async def _upload_local(self, contents: bytes, user_id: uuid.UUID, filename: str) -> str:
        """로컬 파일 시스템에 업로드 (개발용)"""
        # 사용자별 폴더 생성
        user_dir = self.upload_dir / str(user_id)
        user_dir.mkdir(exist_ok=True)

        # 파일 저장
        new_filename = self._generate_filename(user_id, filename)
        file_path = user_dir / new_filename
        
        with open(file_path, "wb") as f:
            f.write(contents)

        # 개발 환경 URL 반환 (API 서버에서 정적 파일 서빙)
        return f"/uploads/{user_id}/{new_filename}"

    async def _upload_s3(self, contents: bytes, user_id: uuid.UUID, filename: str, content_type: str) -> str:
        """S3에 업로드 (운영용)"""
        key = self._generate_key(user_id, filename)

        try:
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=contents,
                ContentType=content_type,
            )
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"파일 업로드 실패: {str(e)}",
            )

        # URL 생성
        if settings.AWS_S3_ENDPOINT_URL:
            # Local development (MinIO)
            return f"{settings.AWS_S3_ENDPOINT_URL}/{self.bucket}/{key}"
        else:
            return f"https://{self.bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

    async def delete_image(self, image_url: str) -> bool:
        """이미지 삭제"""
        if self.is_dev:
            return await self._delete_local(image_url)
        else:
            return await self._delete_s3(image_url)

    async def _delete_local(self, image_url: str) -> bool:
        """로컬 파일 삭제 (개발용)"""
        try:
            # URL에서 경로 추출: /uploads/user_id/filename
            relative_path = image_url.lstrip("/")
            file_path = Path(relative_path)
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception:
            return False

    async def _delete_s3(self, image_url: str) -> bool:
        """S3 파일 삭제 (운영용)"""
        try:
            # URL에서 키 추출
            if settings.AWS_S3_ENDPOINT_URL:
                key = image_url.replace(f"{settings.AWS_S3_ENDPOINT_URL}/{self.bucket}/", "")
            else:
                key = image_url.split(f".amazonaws.com/")[-1]

            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False
