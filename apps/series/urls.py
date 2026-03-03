from django.urls import path

from apps.series.views.page_views import series_my_list_page, series_detail_page
from apps.series.views.series_api import SeriesAPIView
from apps.series.views.series_manage_api import SeriesDetailAPIView

urlpatterns = [
    # [API 라우팅]
    path("my/", SeriesAPIView.as_view(), name="series_my_list_create"),
    path(
        "my/<int:series_id>/",
        SeriesDetailAPIView.as_view(),
        name="series_detail_manage",
    ),
    # [화면 라우팅]
    path("my/page/", series_my_list_page, name="series_my_list_page"),
    path("<int:series_id>/page/", series_detail_page, name="series_detail_page"),
]
