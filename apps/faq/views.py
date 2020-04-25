from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from apps.faq.models import FAQ
from apps.questions.forms import QuestionForm
from django.contrib import messages
from django.utils.translation import gettext as _


class FAQListView(FormMixin, ListView):
    model = FAQ
    template_name = 'faq/list.html'
    context_object_name = 'faqs'
    ordering = ['created_at']
    paginate_by = 10
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        # From BaseListView
        self.object_list = self.get_queryset()
        context = self.get_context_data(
            object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        self.object_list = self.get_queryset()
        if form.is_valid():
            form.save()
            messages.success(
                request,
                _('Your question has been sent successfully'))
            if self.request.GET.get('page') and int(self.request.GET.get('page')) > 1:
                return redirect(reverse('faq:list') + '?page=' + self.request.GET.get('page'))
            else:
                return redirect('faq:list')
        return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))
