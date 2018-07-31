from django import forms
from django.contrib.auth.models import User
from blog.models import Post


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content"
        ]