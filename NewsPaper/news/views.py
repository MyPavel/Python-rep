from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    ordering = ['-date']
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(ListView):
    model = Post
    ordering = ['-date']
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    # подписка
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in self.get_object().Category.all():
                context['is_subscribe'] = self.request.user.category_set.filter(pk=category.pk).exists()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post')
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.postAuthor = Author.objects.get(
            authorUser=self.request.user
        )
        self.object.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post')


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post')


@login_required
def add_subscribe(request, **kwargs):
    category_number = int(kwargs['pk'])
    Category.objects.get(pk=category_number).subscribers.add(request.user)
    return redirect('/posts/')


@login_required
def del_subscribe(request, **kwargs):
    category_number = int(kwargs['pk'])
    Category.objects.get(pk=category_number).subscribers.remove(request.user)
    return redirect('/posts/')
