from card_types.models import (CardType,
                               FOR_FULL_MONTH, FOR_SOME_LESSONS, FOR_TRAINING_COURSE, FOR_TRIAL)


def get_price(yoga_class, card_type):
    if card_type.form_of_using == FOR_FULL_MONTH:
        return yoga_class.get_price_per_month()
    if card_type.form_of_using == FOR_SOME_LESSONS:
        return yoga_class.get_price_per_lesson()
    if card_type.form_of_using == FOR_TRIAL:
        return yoga_class.get_trial_price()
    return yoga_class.get_price_course()


def get_total_price(yoga_class, card_type, number_of_lessons):
    # FULL MONTH = price month
    if card_type.form_of_using == FOR_FULL_MONTH:
        return yoga_class.get_price_per_month()
    # FOR SOME LESSONS = number_of_lessons * price
    if card_type.form_of_using == FOR_SOME_LESSONS:
        total_price = yoga_class.price_per_lesson * number_of_lessons
        return total_price
    if card_type.form_of_using == FOR_TRIAL:
        if yoga_class.price_per_lesson is not None and yoga_class.price_per_lesson == 0:
            return _('Free')
        if card_type.multiplier is not None and card_type.multiplier > 0:
            if yoga_class.price_per_lesson is not None:
                total_price = yoga_class.price_per_lesson * \
                    card_type.multiplier * number_of_lessons
                return total_price
            else:
                return _('have not updated yet')
        else:
            return _('Free')
    return yoga_class.price_course


def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False
