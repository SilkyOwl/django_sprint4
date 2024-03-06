from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserChangeForm

from .models import Comment, Post

from django.contrib.auth.models import User


class CreatePostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        initial=timezone.now,
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            },
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "image",
            "text",
            "pub_date",
            "location",
            "category",
            "is_published",
        )


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)


class UserForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]
