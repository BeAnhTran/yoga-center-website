from django.shortcuts import render
from django.views.generic.list import ListView

from apps.faq.models import FAQ


class FAQListView(ListView):
    model = FAQ
    template_name = 'faq/list.html'
    context_object_name = 'faqs'
    ordering = ['created_at']
    paginate_by = 10
