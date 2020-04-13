from django.shortcuts import render, redirect, reverse
from core.models import Trainer
from lessons.models import Lesson
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required, staff_required
from teach.models import TrainerLesson, TAUGHT_STATE, TAUGHT_INSTEAD_STATE
from django.db import transaction


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
    else:
        if lesson.yogaclass.trainer == trainer:
            state = TAUGHT_STATE
        elif lesson.substitute_trainer is not None and lesson.substitute_trainer == trainer:
            state = TAUGHT_INSTEAD_STATE
        TrainerLesson.objects.create(
            lesson=lesson, trainer=trainer, state=state)
    return redirect('dashboard:lessons-roll-calls', pk=lesson_id)
