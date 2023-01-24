from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Article, Response


class ArticleList(ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'articles'


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'
    queryset = Article.objects.all()