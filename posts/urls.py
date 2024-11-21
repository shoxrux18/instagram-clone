from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PostListCreateView.as_view(),
    ),
    path(
        "<int:pk>/",
        views.PostRetrieveUpdateView.as_view(),
    ),
    path(
        "<int:pk>/like/",
        views.PostLikeView.as_view(),
    ),
    path(
        "<int:pk>/comments/",
        views.PostCommentListCreateView.as_view(),
    ),
    path(
        "comments/delete/<int:pk>/",
        views.CommentDeleteView.as_view(),
    ),
    path(
        "comments/<int:pk>/reply/",
        views.CommentReplyCreateView.as_view(),
    ),
    path(
        "comments/<int:pk>/like/",
        views.CommentLikeView.as_view(),
    ),
    path(
        "comments/<int:pk>/delete-like/",
        views.CommentLikeView.as_view(),
    ),
    path(
        "<int:pk>/stories/",
        views.StoryListCreateView.as_view(),
    ),
    path(
        "stories/",
        views.StoryListCreateView.as_view(),
    ),
    path(
        "story/<int:pk>/",
        views.StoryDetailView.as_view(),
    ),
    path(
        "story/<int:pk>/viewers/",
        views.StoryViewersList.as_view(),
    ),


]
