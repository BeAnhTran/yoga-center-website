from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from ..decorators import admin_required

from classes.models import YogaClass
from ..forms import classes_form

from datetime import datetime
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core import serializers
from django.urls import reverse_lazy


@method_decorator([login_required, admin_required], name='dispatch')
class ClassListView(ListView):
    model = YogaClass
    template_name = 'dashboard/classes/list.html'
    context_object_name = 'classes'
    ordering = ['-updated_at']
    paginate_by = 5


class ClassNewView(View):
    template_name = 'dashboard/classes/new.html'

    def get(self, request):
        form = classes_form.ClassNewForm()
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request, *arg, **kwargs):
        form = classes_form.ClassNewForm(request.POST, request.FILES)
        context = {'form': form}

        if form.is_valid():
            form.save()
            return redirect('dashboard:classes-list')

        return render(request, self.template_name, context=context)


class ClassDetailView(DetailView):
    model = YogaClass
    template_name = 'dashboard/classes/show.html'
    context_object_name = 'yogaclass'


class ClassScheduleView(DetailView):
    model = YogaClass
    template_name = 'dashboard/classes/schedule.html'
    context_object_name = 'yogaclass'


class ClassEditView(UpdateView):
    model = YogaClass
    template_name = 'dashboard/classes/edit.html'
    slug_field = 'slug'
    form_class = classes_form.ClassEditForm

    def get_success_url(self):
            return reverse('dashboard:classes-list', kwargs={})


def get_lessons(request, pk):
    start_date = datetime.fromisoformat(request.GET['startStr'])
    end_date = datetime.fromisoformat(request.GET['endStr'])

    yogaclass = YogaClass.objects.get(pk=pk)
    lessons = yogaclass.lessons.filter(day__range=[start_date, end_date])
    data = serializers.serialize(
        'json', lessons, use_natural_foreign_keys=True)
    return HttpResponse(data, content_type="application/json")


@method_decorator([login_required, admin_required], name='dispatch')
class ClassDeleteView(DeleteView):
    model = YogaClass
    success_url = reverse_lazy('dashboard:classes-list')
