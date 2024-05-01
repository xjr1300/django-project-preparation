from django.apps import AppConfig


class BlogConfig(AppConfig):
    """blogアプリ設定"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.blog"
