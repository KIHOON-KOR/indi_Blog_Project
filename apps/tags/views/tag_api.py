from rest_framework.views import APIView  # API 뷰를 만들기 위한 기본 클래스를 불러옵니다.
from rest_framework.response import Response  # API 응답을 반환하기 위한 클래스를 불러옵니다.
from rest_framework.permissions import AllowAny, IsAuthenticated  # 권한 설정 클래스들을 불러옵니다.
from drf_spectacular.utils import extend_schema  # API 문서화를 위한 데코레이터를 불러옵니다.

from apps.tags.serializers.tag_count_serializer import TagStatSerializer  # 태그 데이터를 JSON으로 바꿔줄 시리얼라이저를 불러옵니다.
from apps.tags.services.tag_count_service import get_tags_with_post_counts  # 위에서 수정한 서비스 함수를 불러옵니다.

class TagListAPIView(APIView):
    # 비회원도 볼 수 있도록 권한을 모두에게 허용
    permission_classes = [AllowAny]

    @extend_schema(tags=["태그"], summary="전체 태그 및 게시글 갯수 통계 조회")
    def get(self, request):
        # 1. 서비스레이어 호출
        tags = get_tags_with_post_counts()

        # 2. 데이터를 JSON으로 변환(여러 개이므로 many=True)
        serializer = TagStatSerializer(tags, many=True)

        return Response(serializer.data)


class MyTagListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["태그"], summary="내가 작성한 글의 태그 통계 조회")
    def get(self, request):
        # 1. 서비스레이어 호출
        tags = get_tags_with_post_counts(user=request.user)

        # 2. 가져온 내 태그 데이터를 JSON 형태로 변환
        serializer = TagStatSerializer(tags, many=True)

        return Response(serializer.data)