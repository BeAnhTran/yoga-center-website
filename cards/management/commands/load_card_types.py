try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.db import transaction


class Command(BaseCommand):
    help = "Load some sample card type into the db"

    @transaction.atomic
    def handle(self, **options):
        from getenv import env
        from cards.models import (CardType, FOR_FULL_MONTH, FOR_CONSECUTIVE_LESSONS,
                                  FOR_NON_CONSECUTIVE_LESSONS, FOR_TRIAL, FOR_TRAINING_COURSE)

        print("Create card types")
        print("Create FOR FULL MONTH card type")
        data_for_full_month = {
            'name': 'học theo tháng',
            'description': 'Áp dụng cho học viên muốn học tất cả các buổi trong tháng',
            'form_of_using': FOR_FULL_MONTH
        }
        full_month_card_type = CardType(**data_for_full_month)
        full_month_card_type.save()

        print("Create FOR CONSECUTIVE LESSONS card type")
        data_for_consecutive_lessons = {
            'name': 'học theo buổi với số buổi liên tiếp',
            'description': 'Áp dụng cho học viên muốn học theo buổi với số buổi đăng kí liên tiếp nhau trong một khoảng thời gian xác định.',
            'form_of_using': FOR_CONSECUTIVE_LESSONS
        }
        consecutive_lessons_card_type = CardType(
            **data_for_consecutive_lessons)
        consecutive_lessons_card_type.save()
        print("Create FOR NON CONSECUTIVE LESSONS card type")
        data_for_non_consecutive_lessons = {
            'name': 'học theo buổi với số buổi không liên tiếp',
            'description': 'Áp dụng cho học viên muốn học theo buổi với số buổi đăng kí không liên tiếp nhau',
            'form_of_using': FOR_NON_CONSECUTIVE_LESSONS,
            'multiplier': env('DEFAULT_MULTIPLIER_FOR_NON_CONSECUTIVE_LESSONS')
        }
        non_consecutive_lessons_card_type = CardType(
            **data_for_non_consecutive_lessons)
        non_consecutive_lessons_card_type.save()
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
