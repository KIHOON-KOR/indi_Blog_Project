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
from botocore.config import Config

class PresignedUrlAPIView(APIView):
    """
    S3에 직접 이미지를 업로드할 수 있는 임시 URL(Presigned URL)을 발급합니다.
    """

    # 이미지는 로그인한(인증된) 사용자만 올릴 수 있도록 제한합니다. (해킹/도배 방지)
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["이미지"],
        summary="S3 Presigned URL 발급",
        parameters=[
            OpenApiParameter(
                name="filename",
                description="업로드할 파일의 원본 이름 (예: my_photo.png)",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
            )
        ],
    )
    def get(self, request):
        # 1. 프론트엔드가 보낸 원본 파일 이름을 가져옵니다.
        filename = request.query_params.get("filename")
        if not filename:
            return Response(
                {"error": "filename은 필수입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 파일 이름 충돌(덮어쓰기)을 막기 위해 고유한 파일명을 생성합니다.
        # 확장자(ext)를 분리한 뒤, 임의의 고유 문자열(uuid)을 붙여줍니다.
        ext = filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4().hex}.{ext}"

        # 3. S3 버킷 내에 저장될 최종 경로를 생성합니다. (예: post/thumbnails/2026/03/08/고유문자열.png)
        today = datetime.now().strftime("%Y/%m/%d")
        object_name = f"post/thumbnails/{today}/{unique_filename}"

        # 4. boto3 S3 클라이언트를 생성합니다. (settings.py에 적어둔 환경변수를 가져옵니다)
        s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4")
        )

        try:
            # 5. 대망의 Presigned URL 생성 부분입니다! (가장 핵심)
            # 'put_object'는 S3에 파일을 올리는 작업을 의미합니다.
            presigned_url = s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                    "Key": object_name,  # 저장될 경로
                    "ContentType": f"image/{ext}",  # 파일 형식 지정 (필수)
                },
                ExpiresIn=600,  # 이 URL의 유효기간을 600초(10분)로 설정합니다. 10분이 지나면 쓸 수 없는 휴지조각이 됩니다.
            )

            # 6. S3에 파일이 저장된 후, 프론트엔드가 사용할 이미지의 최종 접속 주소를 만들어 줍니다.
            # 이 주소를 나중에 게시글 저장 API로 보내게 됩니다.
            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_name}"

            # 7. 프론트엔드에게 임시 업로드 URL과 최종 이미지 URL을 모두 넘겨줍니다.
            return Response(
                {"presigned_url": presigned_url, "image_url": image_url},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
