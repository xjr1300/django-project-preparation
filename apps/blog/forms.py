from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """投稿フォーム"""

    class Meta:
        model = Post
        fields = (
            "title",
            "body",
        )
