from django.urls import path

from apps.series.views.series_api import SeriesAPIView
from apps.series.views.series_manage_api import SeriesDetailAPIView

urlpatterns = [
    # [내 시리즈 목록 조회 및 생성]
    path("my/", SeriesAPIView.as_view(), name="series_my_list_create"),
    path(
        "my/<int:series_id>/",
        SeriesDetailAPIView.as_view(),
        name="series_detail_manage",
    ),
]
