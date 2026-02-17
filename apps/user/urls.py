from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views.login import LoginAPIView
from apps.user.views.page_views import login_page, signup_page
from apps.user.views.signup import SignupAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 브라우저 접속용
    path("login-page/", login_page, name="login_page"),
    path("signup-page/", signup_page, name="signup_page"),
]
