from django.shortcuts import redirect, render
from apps.accounts.models import Trainer
from apps.gallery.models import Gallery
from apps.events.models import Event
from apps.blog.models import Post
from apps.courses.models import Course
from apps.home.forms import SignUpFromHomeForm
from django.views import View


class HomeIndexView(View):
    def get(self, request):
        trainers = Trainer.objects.all()
        gallery = Gallery.objects.first()
        events = Event.objects.all()[:3]
        posts = Post.objects.all()[:3]
        courses = Course.objects.all()
        signup_form_home = SignUpFromHomeForm()
        context = {
            'active_nav': 'home',
            'trainers': trainers,
            'gallery': gallery,
            'events': events,
            'posts': posts,
            'courses': courses,
            'signup_form_home': signup_form_home,
        }
        return render(request, 'home/index.html', context=context)

    def post(self, request):
        signup_form_home = SignUpFromHomeForm(request.POST)
        if signup_form_home.is_valid():
            request.session['sign_up_from_home'] = {}
            request.session['sign_up_from_home']['email'] = signup_form_home.cleaned_data['email']
            request.session['sign_up_from_home']['first_name'] = signup_form_home.cleaned_data['first_name']
            request.session['sign_up_from_home']['last_name'] = signup_form_home.cleaned_data['last_name']
            request.session['sign_up_from_home']['phone_number'] = signup_form_home.cleaned_data['phone_number']
            request.session['sign_up_from_home']['health_condition'] = signup_form_home.cleaned_data['health_condition']
            return redirect('accounts:trainee-signup')
        else:
            trainers = Trainer.objects.all()
            gallery = Gallery.objects.first()
            events = Event.objects.all()[:3]
            posts = Post.objects.all()[:3]
            courses = Course.objects.all()
            signup_form_home = SignUpFromHomeForm()
            context = {
                'active_nav': 'home',
                'trainers': trainers,
                'gallery': gallery,
                'events': events,
                'posts': posts,
                'courses': courses,
                'signup_form_home': signup_form_home,
            }
            return render(request, 'home/index.html', context=context)
