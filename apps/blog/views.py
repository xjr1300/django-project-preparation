from django import forms
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import PostForm
from .models import Post


class PostListView(generic.ListView):
    """投稿一覧ビュー"""

    model = Post

    def get_queryset(self) -> QuerySet[Post]:
        """投稿一覧ビューに表示する投稿を返す。

        投稿一覧ビューに表示する投稿は、現在の日時よりも過去の日時に公開された投稿である。
        また、投稿は、公開日時の昇順に並び替えして返す。

        Returns:
            QuerySet[Post]: 投稿一覧ビューに表示する投稿を格納したクエリセット
        """
        return (
            super()
            .get_queryset()
            .filter(published_at__lte=timezone.now())
            .order_by("published_at")
        )


class PostDetailView(generic.DetailView):
    """投稿詳細ビュー"""

    model = Post


class PostFormMixin(generic.edit.ModelFormMixin):
    """投稿フォームミックスイン"""

    model = Post
    form_class = PostForm

    def get_success_url(self) -> str:
        """リクエストの処理に成功したときにリダイレクト先のURLを返す。

        Returns:
            str: リダイレクト先のURL
        """
        print(f"self.object: {self.object}")
        return reverse(
            "blog:post_detail",
            kwargs={
                "pk": self.object.id,  # type: ignore
            },
        )

    def form_valid(self, form: forms.BaseModelForm) -> HttpResponse:
        """投稿フォームの検証に成功したときの処理をする。

        Args:
            form (forms.BaseModelForm): 投稿ホーム

        Returns:
            HttpResponse: Httpレスポンス
        """
        post = form.save(commit=False)
        post.author = self.request.user  # type: ignore
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


class PostCreateView(PostFormMixin, generic.CreateView):
    """投稿登録ビュー"""


class PostUpdateView(PostFormMixin, generic.UpdateView):
    """投稿更新ビュー"""


class PostDraftListView(generic.ListView):
    """投稿ドラフトリストビュー"""

    model = Post
    template_name = "post_draft_list.html"

    def get_queryset(self) -> QuerySet[Post]:
        """投稿ドラフトリストビューで表示する投稿を返す。

        Returns:
            QuerySet[Post]: 投稿ドラフトリストビューで表示する投稿を格納したクエリセット
        """
        return Post.objects.filter(published_at__isnull=True).order_by("created_at")


class PostPublishView(generic.View):
    """投稿公開ビュー"""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """リクエストを受け取り、投稿の公開日時を設定する。

        Args:
            request (HttpRequest): HTTPリクエスト
            pk (int): 公開する投稿のID

        Returns:
            HttpResponse: HTTPレスポンス
        """
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        return HttpResponseRedirect(reverse("blog:post_detail", kwargs={"pk": pk}))


class PostDeleteView(generic.DeleteView):
    """投稿削除ビュー"""

    model = Post
    success_url = reverse_lazy("blog:post_list")
