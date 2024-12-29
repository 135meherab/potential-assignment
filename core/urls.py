from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentications.urls")),
    # app urls
    path("api/articles/", include("article.urls")),
    path("api/forum/", include("forum.urls")),
    path("api/options/", include("options.urls")),
    path("api/support/", include("support.urls")),
    path("api/settings/", include("site_settings.urls")),
]

if not settings.USE_S3:
    from django.conf.urls.static import static
    from django.views.static import serve

    # serving media and static files
    media_url = [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(
            r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}
        ),
        re_path(
            r"^tinystatic/(?P<path>.*)$", serve, {"document_root": settings.TINYMCE_URL}
        ),
    ]
    urlpatterns += media_url
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    swagger_urlpatterns = [
        path(
            "api/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
        ),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
    urlpatterns += swagger_urlpatterns
    # if app is in debug mode enable django toolbar
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )
