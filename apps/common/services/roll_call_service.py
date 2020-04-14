from apps.roll_calls.models import RollCall
from django.db import transaction


class RollCallService:
    def __init__(self, card, lesson_list):
        self.card = card
        self.lesson_list = lesson_list

    @transaction.atomic
    def call(self):
        if self.lesson_list:
            for lesson in self.lesson_list:
                RollCall.objects.create(card=self.card, lesson=lesson)
        else:
            return
