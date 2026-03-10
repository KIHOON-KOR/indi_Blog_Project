from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.user.services.social_login_service import GithubLoginService, DiscordLoginService
from rest_framework.response import Response
from rest_framework import status


class GithubLoginAPIView(APIView):
    """
    1. 유저가 '깃허브 로그인' 버튼을 눌렀을 때 깃허브 서버로 보내주는 역할만 합니다.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        # 1. settings에 저장된 클라이언트 ID를 가져옵니다.
        client_id = settings.GITHUB_CLIENT_ID

        # 2. 깃허브에 등록한 콜백 주소입니다. (이리로 다시 돌려보내 달라는 뜻)
        redirect_uri = "http://127.0.0.1:8000/api/v1/user/login-page/"

        # 3. 깃허브의 권한 인증 페이지 URL을 만듭니다.
        github_auth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}"

        # 4. 유저의 브라우저를 깃허브 로그인 창으로 강제 이동(리다이렉트) 시킵니다.
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
        client_id = settings.DISCORD_CLIENT_ID
        # urls.py에 등록할 콜백 주소와 동일해야 합니다.
        redirect_uri = "http://127.0.0.1:8000/api/v1/user/login-page/?provider=discord"

        # scope에 identify(프로필)와 email을 필수로 요청합니다.
        discord_auth_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify%20email"

        return redirect(discord_auth_url)


class DiscordLoginCallbackAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 디스코드는 보통 GET 파라미터로 code를 넘겨줍니다 (프론트/백엔드 분리 구조에 따라 POST로 받을 수도 있음)
        code = request.GET.get("code")
        redirect_uri = "http://127.0.0.1:8000/api/v1/user/login-page/?provider=discord"

        if not code:
            return Response(
                {"error": "인가 코드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
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
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)