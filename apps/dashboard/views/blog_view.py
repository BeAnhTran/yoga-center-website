from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views import View

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required

from apps.blog.models import PostCategory, Post
from ..forms import post_categories_form, posts_form

#******************
# POST CATEGORY
#******************


@method_decorator([login_required, admin_required], name='dispatch')
class PostCategoryListView(ListView):
    model = PostCategory
    template_name = 'dashboard/blog/categories/list.html'
    context_object_name = 'categories'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostCategoryListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'blog_categories'
        context['show_nav_blog'] = True
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class PostCategoryNewView(View):
    template_name = 'dashboard/blog/categories/new.html'

    def get(self, request):
        form = post_categories_form.PostCategoryForm()
        context = {
            'form': form,
            'active_nav': 'blog_categories',
            'show_nav_blog': True
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = post_categories_form.PostCategoryForm(
            request.POST, request.FILES)
        context = {
            'form': form,
            'active_nav': 'blog_categories',
            'show_nav_blog': True
        }

        if form.is_valid():
            form.save()
            return redirect('dashboard:blog-categories-list')

        return render(request, self.template_name, context=context)


@method_decorator([login_required, admin_required], name='dispatch')
class PostCategoryDeleteView(DeleteView):
    model = PostCategory
    success_url = reverse_lazy('dashboard:blog-categories-list')

#******************
# POST
#******************


@method_decorator([login_required, admin_required], name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'dashboard/blog/posts/list.html'
    context_object_name = 'posts'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'blog_posts'
        context['show_nav_blog'] = True
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class PostNewView(View):
    template_name = 'dashboard/blog/posts/new.html'

    def get(self, request):
        form = posts_form.PostForm()
        context = {
            'form': form,
            'active_nav': 'blog_posts',
            'show_nav_blog': True
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = posts_form.PostForm(
            request.POST, request.FILES)
        context = {
            'form': form,
            'active_nav': 'blog_posts',
            'show_nav_blog': True
        }

        if form.is_valid():
            form.save()
            return redirect('dashboard:blog-posts-list')

        return render(request, self.template_name, context=context)


@method_decorator([login_required, admin_required], name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('dashboard:blog-posts-list')
