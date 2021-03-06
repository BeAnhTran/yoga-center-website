from django import forms
from apps.lectures.models import Lecture


class LectureInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'autofocus': 'autofocus', 'placeholder': 'tên bài tập'})

    class Meta:
        model = Lecture
        exclude = ()
