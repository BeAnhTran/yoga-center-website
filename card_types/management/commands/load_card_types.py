try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "LOAD SOME SAMPLE <CARD TYPE> INTO THE DATABASE"

    @transaction.atomic
    def handle(self, **options):
        from getenv import env
        from cards.models import (
            CardType, FOR_FULL_MONTH, FOR_SOME_LESSONS, FOR_TRIAL, FOR_TRAINING_COURSE)

        print("Create FOR FULL MONTH card type")
        data_for_full_month = {
            'name': 'học theo tháng',
            'description': 'Áp dụng cho học viên muốn học tất cả các buổi trong tháng',
            'form_of_using': FOR_FULL_MONTH
        }
        full_month_card_type = CardType(**data_for_full_month)
        full_month_card_type.save()

        print("Create FOR SOME LESSONS card type")
        data_for_some_lessons = {
            'name': 'học theo buổi',
            'description': 'Áp dụng cho học viên muốn học theo buổi với số buổi đăng kí trong một khoảng thời gian xác định.',
            'form_of_using': FOR_SOME_LESSONS
        }
        some_lessons_card_type = CardType(
            **data_for_some_lessons)
        some_lessons_card_type.save()

        print("Create FOR TRIAL card type")
        data_for_trial = {
            'name': 'học thử',
            'description': 'Áp dụng cho học viên muốn học thử',
            'form_of_using': FOR_TRIAL,
            'multiplier': env('DEFAULT_MULTIPLIER_FOR_TRIAL')
        }

        trial_card_type = CardType(
            **data_for_trial)
        trial_card_type.save()
        print("Create FOR TRAINING COURSE card type")
        data_for_training_course = {
            'name': 'học theo khóa đào tạo',
            'description': 'Áp dụng cho học viên học khóa học đào tạo',
            'form_of_using': FOR_TRAINING_COURSE
        }

        training_course_card_type = CardType(
            **data_for_training_course)
        training_course_card_type.save()
