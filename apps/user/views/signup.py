from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.user.serializers.signup_serializer import SignupSerializer
from apps.user.services.signup_service import SignupService


class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    @extend_schema(
        tags=["회원관리"],
        summary="회원가입",
        request=SignupSerializer,
    )
    def post(self, request):
        """
        회원가입 요청을 처리합니다.
        """
        # 1. 입력 데이터의 검증
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Service Layer를 호출
        user = SignupService.create_user(serializer.validated_data)

        # 3. 성공적으로 생성 201 Created 응답을 반환
        return Response(
            {
                "message": "회원가입이 성공적으로 완료되었습니다.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "nickname": user.nickname
                }
            },
            status=status.HTTP_201_CREATED
        )