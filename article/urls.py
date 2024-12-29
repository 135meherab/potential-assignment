from django.urls import path
from rest_framework.routers import DefaultRouter

from article.views import (
    ArticleCategoryView,
    ArticleCommentView,
    ArticleLikeView,
    ArticleView,
    HomePageView,
)

router = DefaultRouter()
#  register modelViewSets for articles
router.register("categories", ArticleCategoryView, basename="article-categories")
router.register("", ArticleView, basename="article")

urlpatterns = [
    path("<str:slug>/like/", ArticleLikeView.as_view()),
    path(
        "<str:slug>/comment/",
        ArticleCommentView.as_view(),
    ),
    path("home/", HomePageView.as_view(), name="home-list"),
]
urlpatterns += router.urls
