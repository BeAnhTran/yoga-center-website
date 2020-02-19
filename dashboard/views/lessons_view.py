from django.http import HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dashboard.forms.lesssons_form import LessonForm

from lessons.models import Lesson
from lessons.serializers.lesson_serializer import LessonSerializer


class LessonDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        form = LessonForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            lesson = form.save()
            serializer = LessonSerializer(lesson)
            return Response(serializer.data)
        return HttpResponse(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        lesson = self.get_object(pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
