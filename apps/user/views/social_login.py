from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.user.services.social_login_service import (
    GithubLoginService,
    DiscordLoginService,
)
from rest_framework.response import Response
from rest_framework import status
import urllib.parse
from django.urls import reverse


class GithubLoginAPIView(APIView):
    """
    1. 유저가 '깃허브 로그인' 버튼을 눌렀을 때 깃허브 서버로 보내주는 역할만 합니다.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        # 1. settings에 저장된 클라이언트 ID를 가져옴
        client_id = settings.GITHUB_CLIENT_ID

        # 2. reverse로 'login_page'의 경로를 찾고, build_absolute_uri로 현재 도메인이 포함된 절대 경로를 동적으로 생성
        # 이렇게 하면 로컬/배포 환경에 상관없이 현재 서버의 도메인이 올바르게 반영됨
        redirect_uri = request.build_absolute_uri(reverse("login_page"))

        # 3. 깃허브의 권한 인증 페이지 URL을 만듬
        github_auth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}"

        # 4. 유저의 브라우저를 깃허브 로그인 창으로 강제 이동(리다이렉트) 시킴
        return redirect(github_auth_url)


class GithubLoginCallbackAPIView(APIView):
    """프론트엔드가 넘겨준 코드를 받아 토큰을 발급하는 API (POST)"""

    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response(
                {"error": "인가 코드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. 서비스 호출
            login_data = GithubLoginService.github_login(code)

            # 2. JSON 형태로 토큰 응답 (프론트엔드가 받아서 localStorage에 저장할 데이터)
            return Response(
                {
                    "message": "GitHub 로그인 성공",
                    "token": {
                        "access": login_data["access_token"],
                        "refresh": login_data["refresh_token"],
                    },
                    "user": {
                        "email": login_data["user"].email,
                        "nickname": login_data["user"].nickname,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DiscordLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 디스코드 클라이언트 ID를 가져옴
        client_id = settings.DISCORD_CLIENT_ID

        # 1. 기본 로그인 페이지 URL을 현재 호스트에 맞춰 동적으로 생성
        base_redirect_uri = request.build_absolute_uri(reverse("login_page"))

        # 2. 디스코드 콜백임을 식별하기 위해 쿼리 파라미터를 덧붙임
        redirect_uri = f"{base_redirect_uri}?provider=discord"

        # 3. URL에 들어갈 수 있도록 특수문자(:, /, ? 등)를 안전하게 인코딩
        encoded_redirect_uri = urllib.parse.quote(redirect_uri)

        discord_auth_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={encoded_redirect_uri}&response_type=code&scope=identify%20email"

        return redirect(discord_auth_url)


class DiscordLoginCallbackAPIView(APIView):
    permission_classes = [AllowAny]

    # 프론트엔드가 fetch로 POST 요청을 보내므로 POST로 받음
    def post(self, request):
        # 인가 코드를 가져옵니다.
        code = request.data.get("code")

        # 1. 토큰 요청 시에도 권한 요청 시 보냈던 완벽히 동일한 redirect_uri를 전달해야 함
        # 따라서 현재 환경에 맞는 동적 URL을 다시 한번 만들어 줌
        base_redirect_uri = request.build_absolute_uri(reverse("login_page"))
        redirect_uri = f"{base_redirect_uri}?provider=discord"

        if not code:
            return Response(
                {"error": "인가 코드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 서비스 계층 호출
            login_data = DiscordLoginService.discord_login(code, redirect_uri)

            return Response(
                {
                    "message": "Discord 로그인 성공",
                    "token": {
                        "access": login_data["access_token"],
                        "refresh": login_data["refresh_token"],
                    },
                    "user": {
                        "email": login_data["user"].email,
                        "nickname": login_data["user"].nickname,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            # 에러 발생 시 문자열로 변환하여 프론트엔드로 전달
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
