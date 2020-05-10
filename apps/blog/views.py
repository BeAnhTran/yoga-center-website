from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from apps.blog.models import Post, PostCategory
from django.shortcuts import get_object_or_404
from django.http import Http404


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.request.GET.get('category') is not None:
            category = get_object_or_404(
                PostCategory, slug=self.request.GET['category'])
            return category.posts.all()
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        categories = PostCategory.objects.all()
        newest_posts = Post.objects.all().order_by('-created_at')[:3]
        context['active_nav'] = 'blog'
        context['categories'] = categories
        context['newest_posts'] = newest_posts
        if self.request.GET.get('category') is not None:
            category = get_object_or_404(
                PostCategory, slug=self.request.GET['category'])
            context['category'] = category
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        categories = PostCategory.objects.all()
        newest_posts = Post.objects.all().order_by('-created_at')[:3]
        context['active_nav'] = 'blog'
        context['categories'] = categories
        context['newest_posts'] = newest_posts
        return context
