from apps.card_types.models import (CardType,
                                    FOR_FULL_MONTH, FOR_SOME_LESSONS, FOR_TRAINING_COURSE, FOR_TRIAL, FOR_PERIOD_TIME_LESSONS)
from django.utils.translation import ugettext_lazy as _
from apps.common.templatetags import sexify


def get_price(yoga_class, card_type):
    if card_type.form_of_using == FOR_FULL_MONTH:
        return yoga_class.get_price_per_month()
    elif card_type.form_of_using == FOR_PERIOD_TIME_LESSONS:
        return yoga_class.get_price_per_lesson()
    elif card_type.form_of_using == FOR_SOME_LESSONS:
        return int(float(yoga_class.get_price_per_lesson()) * card_type.multiplier)
    elif card_type.form_of_using == FOR_TRIAL:
        return 0
    return yoga_class.get_price_for_training_course()


def get_total_price(yoga_class, card_type, number_of_lessons):
    # FULL MONTH = price month
    if card_type.form_of_using == FOR_FULL_MONTH:
        return yoga_class.get_price_per_month()
    # FOR SOME LESSONS = number_of_lessons * price
    elif card_type.form_of_using == FOR_PERIOD_TIME_LESSONS:
        total_price = yoga_class.get_price_per_lesson() * number_of_lessons
        return total_price
    elif card_type.form_of_using == FOR_SOME_LESSONS:
        total_price = float(yoga_class.get_price_per_lesson()) * \
            float(number_of_lessons) * card_type.multiplier
        return int(total_price)
    elif card_type.form_of_using == FOR_TRIAL:
        return 0
    else:
        return yoga_class.get_price_for_training_course()


def get_total_price_display(total_price):
    if total_price > 0:
        return sexify.sexy_number(total_price)
    else:
        return _('Free')
