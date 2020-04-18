from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from apps.accounts.models import User


class YogaStory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=225)
    slug = models.SlugField(max_length=250, unique=True)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(YogaStory, self).save(*args, **kwargs)
