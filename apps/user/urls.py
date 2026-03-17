from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views.email_view import EmailSendView, EmailVerifyView
from apps.user.views.login import LoginAPIView
from apps.user.views.page_views import (
    login_page,
    signup_page,
    mypage_view,
    public_profile_page,
    password_reset_page,
)
from apps.user.views.password_view import (
    PasswordResetRequestView,
    PasswordResetConfirmView,
)
from apps.user.views.profile_view import UserProfileAPIView, PublicUserProfileAPIView
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
    # 이메일
    path("email/send/", EmailSendView.as_view(), name="email_send"),
    path("email/verify/", EmailVerifyView.as_view(), name="email_verify"),
    # 비밀번호 찾기
    path(
        "password/reset/request/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # 브라우저 접속용
    path("login-page/", login_page, name="login_page"),
    path("signup-page/", signup_page, name="signup_page"),
    path("mypage/", mypage_view, name="mypage_page"),
    path(
        "profile-page/<str:nickname>/", public_profile_page, name="public_profile_page"
    ),
    path("password-reset-page/", password_reset_page, name="password_reset_page"),
    # 소셜로그인(GitHub)
    path("login/github/", GithubLoginAPIView.as_view(), name="github_login"),
    path(
        "login/github/callback/",
        GithubLoginCallbackAPIView.as_view(),
        name="github_callback",
    ),
    path("garden-stats/", UserGardenStatsAPIView.as_view(), name="user-garden-stats"),
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path(
        "profile/<str:nickname>/",
        PublicUserProfileAPIView.as_view(),
        name="public-user-profile",
    ),
    # 소셜로그인(Discord)
    path("login/discord/", DiscordLoginAPIView.as_view(), name="discord_login"),
    path(
        "login/discord/callback/",
        DiscordLoginCallbackAPIView.as_view(),
        name="discord_callback",
    ),
]
