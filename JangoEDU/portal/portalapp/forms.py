from django import forms
from .models import Article, Response


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'category', 'upload']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']