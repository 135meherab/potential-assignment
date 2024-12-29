from rest_framework.routers import DefaultRouter, path

from forum.views import ForumCommentView, ForumLikeView, ForumViewSets, TagView

router = DefaultRouter()
router.register("tags", TagView, basename="tags")
router.register("", ForumViewSets, basename="forum")

urlpatterns = [
    path("<str:slug>/like/", ForumLikeView.as_view()),
    path(
        "<str:slug>/comment/",
        ForumCommentView.as_view(),
    ),
]
urlpatterns += router.urls
