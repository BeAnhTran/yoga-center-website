from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from .forms import course
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.contrib.auth.decorators import user_passes_test
from courses.models import Course


@staff_member_required(login_url='account_login')
def index(request):
    return render(request, 'dashboard/index.html')


class CourseListView(ListView):
    model = Course
    template_name = 'dashboard/course/list.html'
    context_object_name = 'courses'
    ordering = ['-created_at']
    paginate_by = 5

    @method_decorator(user_passes_test(lambda u: u.is_active and u.is_superuser, login_url='account_login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CourseNewView(View):
    template_name = 'dashboard/course/new.html'
    @method_decorator(user_passes_test(lambda u: u.is_active and u.is_superuser, login_url='account_login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = course.CourseForm()
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = course.CourseForm(request.POST, request.FILES)
        context = {'form': form}

        if form.is_valid():
            form.save()
            return redirect('dashboard:list_course')

        return render(request, self.template_name, context=context)
