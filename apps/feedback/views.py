from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.feedback.forms import FeedbackForm
from django.db import transaction
from rest_framework import status


def create_feedback(request):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse({'success': 'success'}, status=status.HTTP_200_OK)
    return HttpResponse(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)
