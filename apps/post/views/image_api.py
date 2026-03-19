import uuid
import boto3  # type: ignore
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.conf import settings
from datetime import datetime
from botocore.config import Config  # type: ignore


class PresignedUrlAPIView(APIView):
    """
    S3에 직접 이미지를 업로드할 수 있는 임시 URL(Presigned URL)을 발급합니다.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["이미지"],
        summary="S3 Presigned URL 발급",
        parameters=[
            # 1. 원본 파일명을 받기 위한 파라미터
            OpenApiParameter(
                name="filename",
                description="업로드할 파일의 원본 이름 (예: my_photo.png)",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
            ),
            # 2. 이미지가 저장될 도메인(폴더)을 구분하기 위한 파라미터
            OpenApiParameter(
                name="domain",
                description="이미지 사용 목적 (post_thumbnail 또는 profile)",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
        ],
    )
    def get(self, request):
        # 1. 프론트엔드가 보낸 원본 파일 이름을 가져옴
        filename = request.query_params.get("filename")
        if not filename:
            return Response(
                {"error": "filename은 필수입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 프론트엔드에서 보낸 도메인 값을 추출 (기본값은 'post_thumbnail'로 설정하여 하위 호환성 유지)
        domain = request.query_params.get("domain", "post_thumbnail")

        # 3. 파일 이름에서 마지막 '.'을 기준으로 확장자만 분리
        ext = filename.split(".")[-1]
        # 고유한 파일명을 생성하기 위해 uuid4를 사용하고 확장자를 다시 붙임
        unique_filename = f"{uuid.uuid4().hex}.{ext}"

        # 오늘 날짜를 YYYY/MM/DD 형식의 문자열로 만듬
        today = datetime.now().strftime("%Y/%m/%d")

        # 4. 도메인에 따라 S3에 저장될 최종 경로(폴더)를 다르게 설정
        if domain == "profile":
            # 프로필 이미지일 경우 user/profiles 폴더에 저장
            object_name = f"user/profiles/{today}/{unique_filename}"
        else:
            # 기본 게시글 썸네일일 경우 기존 경로를 유지
            object_name = f"post/thumbnails/{today}/{unique_filename}"

        # 5. boto3 S3 클라이언트를 생성 (settings.py에 적어둔 환경변수를 가져옴)
        s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
        )

        try:
            # 6. S3에 파일을 직접 업로드할 수 있는 10분(600초)짜리 임시 URL을 발급
            presigned_url = s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": settings.AWS_STORAGE_BUCKET_NAME,  # 저장될 버킷 이름
                    "Key": object_name,  # 저장될 S3 내의 경로
                    "ContentType": f"image/{ext}",  # 파일의 컨텐츠 타입
                },
                ExpiresIn=600,  # 이 URL의 유효기간을 600초(10분)로 설정합니다. 10분이 지나면 쓸 수 없는 휴지조각이 됩니다.
            )

            # 7. S3에 파일이 저장된 후, 업로드가 완료된 후 프론트엔드가 DB에 저장 요청을 보낼 때 사용할 실제 이미지 URL
            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_name}"

            # 8. 발급받은 임시 URL과 최종 URL을 클라이언트에게 응답
            return Response(
                {"presigned_url": presigned_url, "image_url": image_url},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
