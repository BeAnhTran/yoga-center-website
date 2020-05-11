import random
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from ..decorators import staff_required
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Trainee, TemporaryLeaveRequest
from apps.cards.models import ExtendCardRequest
from apps.refunds.models import Refund
from apps.courses.models import Course
from django.db.models import Count


@login_required
@staff_required
def index(request):
    def r(): return random.randint(0, 255)
    trainees = Trainee.objects.all()
    extend_card_requests = ExtendCardRequest.objects.filter(state=0)
    refund_requests = Refund.objects.filter(state=0)
    temporary_leave_requests = TemporaryLeaveRequest.objects.filter(state=0)
    courses = Course.objects.all().annotate(registrations_count=Count('classes__cards'))
    course_colors = []
    for course in courses:
        course_colors.append('#%02X%02X%02X' % (r(), r(), r()))
    courses_colors = zip(courses, course_colors)
    context = {
        'active_nav': 'dashboard',
        'trainees': trainees,
        'extend_card_requests': extend_card_requests,
        'refund_requests': refund_requests,
        'temporary_leave_requests': temporary_leave_requests,
        'courses': courses,
        'course_colors': course_colors,
        'courses_colors': courses_colors,
    }
    return render(request, 'dashboard/index.html', context=context)
