# `django`プロジェクトの準備方法

- [`django`プロジェクトの準備方法](#djangoプロジェクトの準備方法)
  - [前提事項](#前提事項)
  - [django標準のファイルシステム構成の問題](#django標準のファイルシステム構成の問題)
  - [pythonプロジェクトの準備方法と実装方法との違い](#pythonプロジェクトの準備方法と実装方法との違い)
  - [プロジェクトの作成](#プロジェクトの作成)
  - [`vscode`拡張機能のインストール](#vscode拡張機能のインストール)
  - [最初のマイグレーションの実行](#最初のマイグレーションの実行)
  - [アプリケーションの作成](#アプリケーションの作成)
  - [モデルの実装とマイグレーション](#モデルの実装とマイグレーション)
  - [スーパーユーザーの作成](#スーパーユーザーの作成)
  - [管理サイトへの登録](#管理サイトへの登録)
  - [投稿一覧ページの表示](#投稿一覧ページの表示)
  - [スタイルシートの適用](#スタイルシートの適用)

## 前提事項

- [`python`プロジェクトの準備方法と実装方法](https://github.com/xjr1300/python-project-preparation)が完了していること

## django標準のファイルシステム構成の問題

django標準のファイルシステムの問題を次に示します。

- アプリがプロジェクトディレクトリに作成され、`templates`や`static`などのディレクトリと混在する。
- プロジェクト設定がプロジェクトと同じ名前のディレクトリに作成される。

よって、これらの問題を次の通り解決します。

- アプリを`apps`ディレクトリに集約します。
- プロジェクト設定ファイルを`config`ディレクトリに変更します。

これにより、リンターやフォーマッターが対象とするディレクトリを`apps`と`config`に限定して、設定を変更する必要がなくなります。

## pythonプロジェクトの準備方法と実装方法との違い

`pythonプロジェクトの準備方法と実装方法`と同様ですが次の点が異なります。

- `mypy`を使用しません。
- クラスビューでオーバーライドしたメソッドの型注釈を強制しません。
- ただし、独自に定義したクラス、メソッド、関数及びファイルレベルの変数には、**必ず**`docstring`を記述して、型注釈をしてください。

> `django-stub`などを導入して型注釈することを目指しましたが、うまく動作することができませんでした。
> また、煩雑な割に効果が薄いと判断しました。

## プロジェクトの作成

ターミナルでプロジェクトディレクトリを作成して、そのディレクトリをカレントディレクトリに変更後、そのディレクトリを`vscode`で開きます。

```sh
# `my_project`プロジェクトディレクトリを作成して、そのディレクトリに移動します。
mkdir my_project && cd my_project
# `vscode`を起動します。
code .
```

`vscode`でターミナルを開いて、次のコマンドを実行します。

```sh
# `poetry`でプロジェクトを初期化します。
poetry init
# `django`、`django-debug-toolbar`、`ruff`、`pre-commit`をインストールします。
poetry add django django-debug-toolbar ruff pre-commit
# カレントディレクトリにdjangoプロジェクトを作成します。
poetry run django-admin startproject my_project .
# プロジェクトディレクトリに`.gitignore`を作成します（内容は後述）。
code .gitignore
# gitリポジトリを初期化
git init
# `pyproject.toml`ファイルを編集します(内容は後述)。
code pyproject.toml
# `.pre-commit-config.yaml`ファイルを作成します (内容は後述)。
code .pre-commit-config.yaml
# `pre-commit`を有効化
poetry run pre-commit install
# `my_project`ディレクトリを`config`に名前を変更します。
mv my_project config
# `manage.py`を編集します（内容は後述）。
code manage.py
# `config/settings.py`を編集します（内容は後述）。
code config/settings.py
# `config/urls.py`を編集をします（内容は後述）。
code config/urls.py
# `config/wsgi.py`と`config/asgi.py`を編集します（内容は後述）。
code config/wsgi.py
code config/asgi.py
# django開発サーバーが起動することを確認します。
# 開発サーバーが正常に起動することを確認できたら、`Ctrl+C`で開発サーバーを終了します。
poetry run python manage.py runserver
```

- `.gitignore`を次の通り作成します。

```text
# python
__pycache__/
*.py[cod]

# distribution / packaging
build/
dist/
sdist/

# unit test / coverage reports
.coverage
.coverage.*
.cache
coverage.xml

# translations
*.mo
*.pot

# sphinx documentation
docs/_build/

# dotenv
.env

# virtual environment
.venv/
venv/

# ruff
.ruff_cache/

# mypy
.mypy_cache/

# django
db.sqlite3
assets/
```

- `pyproject.toml`に次を追加します。

```toml
[tool.ruff]

# モジュールディレクトリとテストディレクトリ
src = ["apps", "config", "tests"]

# マイグレーションディレクトリを除外
exclude = ["migrations"]

# 1行の最大文字数
line-length = 88

[tool.ruff.lint]

select = [
  "F", # pyflakes
  "E", # pycodestyle
  "W", # pycodestyle warnings
  "I", # isort
  "D", # pydocstyle
]

ignore = [
  "D100", # undocumented-public-module
  "D104", # undocumented-public-package
  "D106", # undocumented-public-nested-class
  "D212", # multi-line-summary-first-line
  "D415", # ends-in-punctuation
]

extend-ignore = []

[tool.ruff.lint.pydocstyle]
# docstringはgoogle style
convention = "google"
```

- `.pre-commit-config.yaml`を次の通り作成します（`hooks`に`mypy`がないことに注意）。

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.2 # ruffバージョン
    hooks:
      # リンターの実行
      - id: ruff
        name: lint with ruff
      - id: ruff
        name: sort imports with ruff
        args: [--select, I, --fix]
      # フォーマッターの実行
      - id: ruff-format
        name: format with ruff
```

- `manage.py`を次の通り変更します。

```python
 #!/usr/bin/env python
 """Django's command-line utility for administrative tasks."""
 import os
 import sys


 def main():
     """Run administrative tasks."""
-    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
+    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
     try:
         from django.core.management import execute_from_command_line
     except ImportError as exc:
```

- `config/settings.py`を次の通り変更します。

```python
+import os
 from pathlib import Path
+from typing import List, Dict

# snip

-ALLOWED_HOSTS = []
+ALLOWED_HOSTS: List[str] = []

+INTERNAL_IPS: List[str] = ["127.0.0.1", "localhost"]

 # Application definition

 INSTALLED_APPS = [
     "django.contrib.admin",
     "django.contrib.auth",
     "django.contrib.contenttypes",
     "django.contrib.sessions",
     "django.contrib.messages",
     "django.contrib.staticfiles",
+    "debug_toolbar",
 ]

 MIDDLEWARE = [
+    "debug_toolbar.middleware.DebugToolbarMiddleware",
     "django.middleware.security.SecurityMiddleware",
     "django.contrib.sessions.middleware.SessionMiddleware",
     "django.middleware.common.CommonMiddleware",
     "django.middleware.csrf.CsrfViewMiddleware",
     "django.contrib.auth.middleware.AuthenticationMiddleware",
     "django.contrib.messages.middleware.MessageMiddleware",
     "django.middleware.clickjacking.XFrameOptionsMiddleware",
 ]

-ROOT_URLCONF = "my_project.urls"
+ROOT_URLCONF = "config.urls"

-TEMPLATES = [
+TEMPLATES: List[Dict[str, str | bool | List[str] | Dict[str, List[str]]]] = [

# snip

-WSGI_APPLICATION = "my_project.wsgi.application"
+WSGI_APPLICATION = "config.wsgi.application"

# snip

-LANGUAGE_CODE = "en-us"
+LANGUAGE_CODE = "ja"

-TIME_ZONE = "UTC"
+TIME_ZONE = "Asia/Tokyo"

 USE_I18N = True

 USE_TZ = True


 # Static files (CSS, JavaScript, Images)
 # https://docs.djangoproject.com/en/5.0/howto/static-files/
 STATIC_URL = "static/"

+STATIC_ROOT = os.path.join(BASE_DIR, "assets")
```

- `config/urls.py`を次の通り変更します。

```python
 from django.contrib import admin
-from django.urls import path
+from django.urls import include, path

 urlpatterns = [
+    path("__debug__/", include("debug_toolbar.urls")),
     path("admin/", admin.site.urls),
 ]
```

- `config/wsgi.py`、`config/asgi.py`を次の通り変更します。

```python
-os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
+os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```

## `vscode`拡張機能のインストール

`vscode`に`Django`と`Django Template Support`拡張機能をインストールします。

djangoのテンプレートをフォーマットするために、`.vscode/settings.json`を作成して、次を入力します。

```json
{
  "files.associations": {
    "apps/templates/**/*.html": "django-html",
    "templates/**/*.html": "django-html",
  },
  "[django-html]": {
    "editor.defaultFormatter": "junstyle.vscode-django-support",
    "editor.tabSize": 2,
  },
}
```

## 最初のマイグレーションの実行

```sh
# 最初のマイグレーションを実行します。
poetry run python manage.py migrate
```

## アプリケーションの作成

次の通り、`apps/blog`ディレクトリを作成後、そのディレクトリを指定して`blog`アプリケーションを作成します。

```sh
mkdir -p apps/blog
poetry run python manage.py startapp blog apps/blog
```

次の通り、`apps/blog/apps.py`ファイルを変更します。

```python
# apps/blog/apps.py
 from django.apps import AppConfig


 class BlogConfig(AppConfig):
     """blogアプリ設定"""

     default_auto_field = "django.db.models.BigAutoField"
-    name = "blog"
+    name = "apps.blog"
```

次の通り、`config/settings.py`ファイルを変更します。

```python
 INSTALLED_APPS = [
     "django.contrib.sessions",
     "django.contrib.messages",
     "django.contrib.staticfiles",
+    "apps.blog.apps.BlogConfig",
 ]
```

## モデルの実装とマイグレーション

次の通り`Post`モデルを実装します。

```python
# apps/blog/models.py
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
```

次の通りマイグレーションを実行します。

```sh
# マイグレーションファイルを作成
poetry run python manage.py makemigrations blog
# マイグレーションを実行
poetry run python manage.py migrate
```

## スーパーユーザーの作成

次の通りスーパーユーザーを作成します。

```sh
% poetry run python manage.py createsuperuser
ユーザー名 (leave blank to use 'xjr1300'): django
メールアドレス: django@example.com
Password:
Password (again):
Superuser created successfully.
```

## 管理サイトへの登録

次の通り、`apps/blog/admin.py`ファイルを変更して、`Post`モデルを管理サイトに登録します。

```python
from django.contrib import admin

from .models import Post

admin.site.register(Post)
```

## 投稿一覧ページの表示

次の通り実装します。

- `apps/blog/views.py`

```python
from django.db.models import QuerySet
from django.utils import timezone
from django.views import generic

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
```

- `apps/blog/templates/blog/post_list.html`

```html
<html>
  <head>
    <title>Django Girls blog</title>
  </head>
  <body>
    <div>
      <h1><a href="/">Django Girls Blog</a></h1>
    </div>
    {% for post in object_list %}
    <div>
      <p>公開日時: {{ post.published_at }}</p>
      <h2><a href="">{{ post.title }}</a></h2>
      <p>{{ post.body|linebreaksbr }}</p>
    </div>
    {% endfor %}
  </body>
</html>
```

- `apps/blog/urls.py`

```python
from typing import List

from django.urls import URLPattern, path

from . import views

urlpatterns: List[URLPattern] = [
    path("", views.PostListView.as_view(), name="post_list")
]
```

## スタイルシートの適用

次の通りスタイルシートを適用します。

- `apps/blog/static/css/blog.css`

```css
body {
  padding-left: 15px;
}

h1 a,
h2 a {
  color: #c25100;
  font-family: "Lobster";
}

.page-header {
  background-color: #c25100;
  margin-top: 0;
  padding: 20px 20px 20px 40px;
}

.page-header h1,
.page-header h1 a,
.page-header h1 a:visited,
.page-header h1 a:active {
  color: #ffffff;
  font-size: 36pt;
  text-decoration: none;
}

.content {
  margin-left: 40px;
}

h1,
h2,
h3,
h4 {
  font-family: "Lobster", cursive;
}

.date {
  color: #828382;
}

.save {
  float: right;
}

.post-form textarea,
.post-form input {
  width: 100%;
}

.top-menu,
.top-menu:hover,
.top-menu:visited {
  color: #ffffff;
  float: right;
  font-size: 26pt;
  margin-right: 20px;
}

.post {
  margin-bottom: 70px;
}

.post h2 a,
.post h2 a:visited {
  color: #000000;
}
```

- `apps/blog/templates/blog/post_list.html`

```html
{% load static %}
<html>
  <head>
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"
    />
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"
    />
    <link
      href="//fonts.googleapis.com/css?family=Lobster&subset=latin,latin-ext"
      rel="stylesheet"
      type="text/css"
    />
    <link rel="stylesheet" href="{% static 'css/blog.css' %}" />
    <title>Django Girls blog</title>
  </head>
  <body>
    <div class="page-header">
      <h1><a href="/">Django Girls Blog</a></h1>
    </div>
    <div class="content container">
      <div class="row">
        <div class="col-md-8">
          {% for post in object_list %}
          <div class="post">
            <div class="date">
              <p>公開日時: {{ post.published_at }}</p>
            </div>
            <h2><a href="">{{ post.title }}</a></h2>
            <p>{{ post.body|linebreaksbr }}</p>
          </div>
          {% endfor %}
        </div>
      </div>
    </div>
  </body>
</html>
```
