from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from blog.models import Post, PostCategory
from django.shortcuts import get_object_or_404
from django.http import Http404


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'blog'
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['active_nav'] = 'blog'
        return context
