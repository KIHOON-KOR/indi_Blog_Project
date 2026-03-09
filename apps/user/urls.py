from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views.login import LoginAPIView
from apps.user.views.page_views import login_page, signup_page
from apps.user.views.signup import SignupAPIView
from apps.user.views.social_login import GithubLoginAPIView, GithubLoginCallbackAPIView

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
]
