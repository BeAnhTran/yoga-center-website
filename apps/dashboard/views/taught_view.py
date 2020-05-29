from django.shortcuts import render, redirect, reverse
from apps.accounts.models import Trainer
from apps.lessons.models import Lesson
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required
from apps.lessons.models import TrainerLesson, TAUGHT_STATE, TAUGHT_INSTEAD_STATE
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


@login_required
@staff_required
@transaction.atomic
def rollCallForTrainer(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    trainer = get_object_or_404(Trainer, pk=request.POST['trainer_id'])

    try:
        taught = TrainerLesson.objects.get(lesson=lesson, trainer=trainer)
    except TrainerLesson.DoesNotExist:
        taught = None

    if taught:
        taught.delete()
        messages.success(request, _('Undo the call successfully'))
    else:
        if lesson.yogaclass.trainer == trainer:
            state = TAUGHT_STATE
        elif lesson.substitute_trainer is not None and lesson.substitute_trainer == trainer:
            state = TAUGHT_INSTEAD_STATE
        TrainerLesson.objects.create(
            lesson=lesson, trainer=trainer, state=state)
        messages.success(request, _('Do the roll call successfully'))
    return redirect('dashboard:lessons-roll-calls', pk=lesson_id)
