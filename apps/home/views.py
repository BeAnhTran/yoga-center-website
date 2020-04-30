from django.shortcuts import redirect, render
# from apps.accounts.models import Trainer
# from apps.gallery.models import Gallery
# from apps.events.models import Event
# from apps.blog.models import Post
# from apps.courses.models import Course


def home(request):
    # trainers = Trainer.objects.all()
    # gallery = Gallery.objects.first()
    # events = Event.objects.all()[:3]
    # posts = Post.objects.all()[:3]
    # courses = Course.objects.all()
    context = {}
    return render(request, 'home/index.html', context=context)
