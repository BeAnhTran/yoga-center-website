from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from classes.models import YogaClass
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from datetime import datetime
from django.utils.formats import get_format
from django.utils import formats
from courses.models import LEVEL_CHOICES
from courses.models import Course
from core.models import Trainer
from django.db.models import Value as V
from django.db.models.functions import Concat


class FilterForm(forms.Form):
    BASIC_LEVEL = 0
    INTERMEDIATE_LEVEL = 1
    ADVANCED_LEVEL = 2
    LEVEL_CHOICES = (
        (None, 'Chọn cấp độ'),
        (BASIC_LEVEL, _('Basic Level')),
        (INTERMEDIATE_LEVEL, _('Intermediate Level')),
        (ADVANCED_LEVEL, _('Advanced Level')),
    )

    QUERY_COURSE = list(((None, 'Chọn khóa học'),)) + \
        list(Course.objects.values_list('slug', 'name'))
    QUERY_TRAINER = list(((None, 'Chọn huấn luyện viên'),)) + list(Trainer.objects.annotate(
        full_name=Concat('user__first_name', V(' '), 'user__last_name')).values_list('user__slug', 'full_name'))
    level = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'circle-select'}),
        choices=LEVEL_CHOICES,
        required=False)
    course = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'circle-select'}),
        choices=QUERY_COURSE,
        required=False)
    trainer = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'circle-select'}),
        choices=QUERY_TRAINER,
        required=False)
