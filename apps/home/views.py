from django.shortcuts import redirect, render
from apps.accounts.models import Trainer
from apps.events.models import Event
from apps.blog.models import Post
from apps.courses.models import Course
from apps.home.forms import SignUpFromHomeForm
from django.views import View
from apps.feedback.forms import FeedbackForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class HomeIndexView(View):
    def get(self, request):
        trainers = Trainer.objects.all()
        events = Event.objects.all()[:3]
        posts = Post.objects.all()[:3]
        courses = Course.objects.all()
        signup_form_home = SignUpFromHomeForm()
        context = {
            'active_nav': 'home',
            'trainers': trainers,
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
            events = Event.objects.all()[:3]
            posts = Post.objects.all()[:3]
            courses = Course.objects.all()
            signup_form_home = SignUpFromHomeForm()
            context = {
                'active_nav': 'home',
                'trainers': trainers,
                'events': events,
                'posts': posts,
                'courses': courses,
                'signup_form_home': signup_form_home,
            }
            return render(request, 'home/index.html', context=context)


class AboutUsView(View):
    def get(self, request):
        context = {
            'active_nav': 'about-us'
        }
        return render(request, 'home/about_us.html', context=context)


class ContactView(View):
    def get(self, request):
        form = FeedbackForm()
        context = {
            'form': form,
            'active_nav': 'about-us'
        }
        return render(request, 'home/contact.html', context=context)

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Send feedback successfully'))
            return redirect('home:contact')
        context = {
            'form': form,
        }
        return render(request, 'home/contact.html', context=context)