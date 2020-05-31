import random
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from ..decorators import staff_required
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Trainee, TemporaryLeaveRequest
from apps.refunds.models import Refund
from apps.courses.models import Course
from django.db.models import Count
from apps.card_invoices.models import CardInvoice


@login_required
@staff_required
def index(request):
    def r(): return random.randint(0, 255)
    trainees = Trainee.objects.all()
    refund_requests = Refund.objects.filter(state=0)
    temporary_leave_requests = TemporaryLeaveRequest.objects.filter(state=0)
    courses = Course.objects.all().annotate(registrations_count=Count('classes__cards'))
    course_colors = []
    for course in courses:
        course_colors.append('#%02X%02X%02X' % (r(), r(), r()))
    courses_colors = zip(courses, course_colors)
    earning = 0
    unpaid_card_count = 0
    for c in CardInvoice.objects.all():
        if c.is_charged():
            earning += c.amount
        else:
            unpaid_card_count+=1
    context = {
        'active_nav': 'dashboard',
        'trainees': trainees,
        'refund_requests': refund_requests,
        'temporary_leave_requests': temporary_leave_requests,
        'courses': courses,
        'course_colors': course_colors,
        'courses_colors': courses_colors,
        'earning': earning,
        'unpaid_card_count': unpaid_card_count
    }
    return render(request, 'dashboard/index.html', context=context)
