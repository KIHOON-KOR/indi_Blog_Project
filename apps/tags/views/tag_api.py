from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from apps.tags.serializers.tag_count_serializer import TagStatSerializer
from apps.tags.services.tag_count_service import get_tags_with_post_counts


class TagListAPIView(APIView):
    """홈 화면 등에 쓰일 전체 태그 목록 및 통계를 제공합니다."""

    # 홈 화면 데이터이므로 로그인하지 않은 유저(비회원)도 볼 수 있게 AllowAny로 설정합니다.
    permission_classes = [AllowAny]

    @extend_schema(tags=["태그"], summary="전체 태그 및 게시글 갯수 통계 조회")
    def get(self, request):
        # 1. 서비스 레이어 호출
        tags = get_tags_with_post_counts()

        # 2. 시리얼라이저를 통해 JSON 형태로 변환
        serializer = TagStatSerializer(tags, many=True)

        return Response(serializer.data)
