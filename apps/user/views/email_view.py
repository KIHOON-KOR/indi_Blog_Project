from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.user.serializers.email_serializer import EmailSendSerializer, EmailVerifySerializer
from apps.user.services.email_service import EmailVerificationService


class EmailSendView(APIView):
    """이메일 발송 요청을 처리하는 API 뷰"""
    def post(self, request):
        # 1. 입력데이터 검증
        serializer = EmailSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 무사히 검사를 통과한 깨끗한 이메일 데이터를 꺼내옴
        email = serializer.validated_data.get("email")
        # 3. 서비스 레이어 호출
        EmailVerificationService.send_verification_code(email)

        return Response(
            {"message": "인증번호가 이메일로 발송되었습니다."},
            status=status.HTTP_200_OK
        )


class EmailVerifyView(APIView):
    """# 사용자가 입력한 인증번호를 검증하는 API 뷰"""
    def post(self, request):
        # 1. 입력데이터 검증
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 검사를 통과한 이메일을 꺼냅니다.
        email = serializer.validated_data.get("email")
        # 3. # 검사를 통과한 6자리 인증번호를 꺼냅니다.
        code = serializer.validated_data.get("code")

        # 4. 서비스레이어 호출
        is_verified = EmailVerificationService.verify_code(email,code)

        if is_verified:
            return Response(
                {"message": "이메일 인증이 완료되었습니다."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "인증번호가 일치하지 않거나 만료되었습니다."},
            status=status.HTTP_400_BAD_REQUEST
        )