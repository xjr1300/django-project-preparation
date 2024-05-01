from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    """投稿モデル"""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="投稿者"
    )
    title = models.CharField("タイトル", max_length=200)
    body = models.TextField("本文")
    created_at = models.DateTimeField("投稿日時", default=timezone.now)
    published_at = models.DateTimeField("公開日時", blank=True, null=True)

    def publish(self) -> None:
        """投稿を公開する。"""
        self.published_at = timezone.now()
        self.save()

    def __str__(self) -> str:
        """タイトルを返す。

        Returns:
            str: タイトル
        """
        return self.title
