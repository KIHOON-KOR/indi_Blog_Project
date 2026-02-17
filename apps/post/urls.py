from django.urls import path

# 페이지 렌더링을 위한 HTML 뷰를 가져옵니다.
from apps.post.views.page_views import post_write_page

# API 처리를 위한 클래스 기반 뷰(CBV)들을 가져옵니다.
from apps.post.views.post_api import PostAPIView, MyPostAPIView, MyTempPostAPIView

urlpatterns = [
    # [전체 피드 및 생성]
    path("", PostAPIView.as_view(), name="post_list_create"),
    # [내 블로그]
    path("my/", MyPostAPIView.as_view(), name="post_my_list"),
    # [임시글 관리]
    path("my/temp/", MyTempPostAPIView.as_view(), name="post_temp_list"),
    path(
        "my/temp/<int:post_id>/", MyTempPostAPIView.as_view(), name="post_temp_manage"
    ),
    # [화면(UI)]
    path("write/", post_write_page, name="post_write_page"),
]
