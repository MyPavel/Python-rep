from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Article, Response
from .forms import ArticleForm, ResponseForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .filters import ArticleFilter
from django.shortcuts import redirect


def ap_response(request, pk):
    my_responses = Response.objects.get(id=pk)
    my_responses.status = True
    my_responses.save()
    return redirect('responses')


def del_response(request, pk):
    my_responses = Response.objects.get(id=pk)
    my_responses.delete()
    return redirect('responses')


class ArticleList(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10
    ordering = ['-date']


class ArticleDetail(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'
    queryset = Article.objects.all()


class ArticleCreate(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article_create.html'
    success_url = reverse_lazy('article_list')

    # Автоматически заполняем поле автора = пользователь
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    permission_required = 'portalapp.delete_article'


class ResponseAdd(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'response.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.article = Article.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(form)


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    context_object_name = 'responses'
    paginate_by = 10
    template_name = 'responses.html'

    def get_queryset(self, **kwargs):
        queryset = Response.objects.filter(article__author=self.request.user)
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

