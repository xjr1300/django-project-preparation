from typing import List

from django.urls import URLPattern, path

from . import views

app_name = "blog"

urlpatterns: List[URLPattern] = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("drafts/", views.PostDraftListView.as_view(), name="post_draft_list"),
    path(
        "post/<int:pk>/publish/", views.PostPublishView.as_view(), name="post_publish"
    ),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]
