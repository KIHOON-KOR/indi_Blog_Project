from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularAPIView,
)

urlpatterns: list[URLPattern | URLResolver] = [
    path("", include("apps.core.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("apps.user.urls")),
    path("api/v1/post/", include("apps.post.urls")),
    path("api/v1/tags/", include("apps.tags.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "drf_spectacular" in settings.INSTALLED_APPS:
        urlpatterns += [
            # 1. 코드를 읽고 자동으로 스키마를 생성하는 뷰
            path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
            # 2. Swagger UI 설정 수정
            path(
                "api/schema/swagger-ui/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="swagger-ui",
            ),
            path(
                "api/schema/redoc/",
                SpectacularRedocView.as_view(url_name="schema"),
                name="redoc",
            ),
        ]
