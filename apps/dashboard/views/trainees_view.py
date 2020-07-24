from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import staff_required

from apps.accounts.models import Trainee
from apps.dashboard.forms.trainees_form import TraineeForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from apps.classes.models import YogaClass
from apps.courses.models import TRAINING_COURSE


@method_decorator([login_required, staff_required], name='dispatch')
class TraineeListView(ListView):
    model = Trainee
    template_name = 'dashboard/trainees/list.html'
    context_object_name = 'trainees'
    ordering = ['user__date_joined']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(TraineeListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'trainees'
        context['show_nav_users'] = True
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class TraineeNewView(View):
    template_name = 'dashboard/trainees/new.html'

    def get(self, request):
        context = {}
        form = TraineeForm()
        context['form'] = form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = TraineeForm(request.POST, request.FILES)
        context = {}
        context['form'] = form
        if form.is_valid():
            with transaction.atomic():
                trainee = form.save(request)
                messages.success(self.request, _(
                    'Create new trainee successfully'))
                if request.GET.get('next') is not None:
                    next_str = request.GET.get('next')
                    return redirect(self.request.GET.get('next') + '&trainee-id=' + str(trainee.pk))
                else:
                    return redirect('dashboard:trainees-list')
        context['active_nav'] = 'trainees'
        context['show_nav_users'] = True
        return render(request, self.template_name, context=context)


@method_decorator([login_required, staff_required], name='dispatch')
class TraineeOfTrainingClassListView(ListView):
    model = Trainee
    template_name = 'dashboard/trainees/training-class/list.html'
    context_object_name = 'trainees'
    ordering = ['user__date_joined']
    paginate_by = 10

    def get_queryset(self):
        if self.kwargs.get('slug'):
            yoga_class = YogaClass.objects.filter(
                course__course_type=TRAINING_COURSE, slug=self.kwargs.get('slug')).first()
            if yoga_class is not None:
                trainees = Trainee.objects.filter(
                    cards__yogaclass=yoga_class).distinct()
                return trainees
            else:
                return []
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(TraineeOfTrainingClassListView,
                        self).get_context_data(**kwargs)
        yoga_class = YogaClass.objects.filter(
                course__course_type=TRAINING_COURSE, slug=self.kwargs.get('slug')).first()
        context['active_nav'] = 'trainees-of-training-class'
        context['show_nav_users'] = True
        context['yoga_class'] = yoga_class
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class TrainingClassListView(ListView):
    model = YogaClass
    template_name = 'dashboard/trainees/training-class/index.html'
    context_object_name = 'classes'
    paginate_by = 10

    def get_queryset(self):
        return YogaClass.objects.filter(course__course_type=TRAINING_COURSE).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(TrainingClassListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'trainees-of-training-class'
        context['show_nav_users'] = True
        return context
