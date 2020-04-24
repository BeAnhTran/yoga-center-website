from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
