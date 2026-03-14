from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views.login import LoginAPIView
from apps.user.views.page_views import login_page, signup_page
from apps.user.views.signup import SignupAPIView
from apps.user.views.social_login import (
    GithubLoginAPIView,
    GithubLoginCallbackAPIView,
    DiscordLoginAPIView,
    DiscordLoginCallbackAPIView,
)
from apps.user.views.users_stat_view import UserGardenStatsAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 브라우저 접속용
    path("login-page/", login_page, name="login_page"),
    path("signup-page/", signup_page, name="signup_page"),
    # 소셜로그인(GitHub)
    path("login/github/", GithubLoginAPIView.as_view(), name="github_login"),
    path(
        "login/github/callback/",
        GithubLoginCallbackAPIView.as_view(),
        name="github_callback",
    ),
    path("garden-stats/", UserGardenStatsAPIView.as_view(), name="user-garden-stats"),
    # 소셜로그인(Discord)
    path("login/discord/", DiscordLoginAPIView.as_view(), name="discord_login"),
    path(
        "login/discord/callback/",
        DiscordLoginCallbackAPIView.as_view(),
        name="discord_callback",
    ),
]
