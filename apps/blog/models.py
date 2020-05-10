from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('published', 'Published')
)


class Post(models.Model):
    category = models.ForeignKey('blog.PostCategory', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=175, unique=True)
    description = models.CharField(max_length=255)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='posts/', null=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class PostCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=175, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PostCategory, self).save(*args, **kwargs)
