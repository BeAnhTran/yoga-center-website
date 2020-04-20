from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from ..forms import gallery_form
from django.utils.decorators import method_decorator
from ..decorators import admin_required
from django.views.generic.list import ListView
from apps.gallery.models import Gallery
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db import transaction


@method_decorator([login_required, admin_required], name='dispatch')
class GalleryListView(ListView):
    model = Gallery
    template_name = 'dashboard/gallery/list.html'
    context_object_name = 'gallery'
    ordering = ['created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['active_nav'] = 'gallery'
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class GalleryNewView(View):
    template_name = 'dashboard/gallery/new.html'

    def get(self, request):
        form = gallery_form.GalleryForm()
        context = {
            'form': form,
            'active_nav': 'gallery'
        }
        if self.request.POST:
            context['gallery_images'] = gallery_form.GalleryImageFormSet(
                self.request.POST, self.request.FILES)
        else:
            context['gallery_images'] = gallery_form.GalleryImageFormSet()
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = gallery_form.GalleryForm(request.POST)
        gallery_images = gallery_form.GalleryImageFormSet(self.request.POST, self.request.FILES)

        with transaction.atomic():
            if form.is_valid():
                obj = form.save()
                if gallery_images.is_valid():
                    gallery_images.instance = obj
                    gallery_images.save()
                return redirect('dashboard:gallery-list')

        context = {
            'form': form,
            'gallery_images': gallery_images
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, admin_required], name='dispatch')
class GalleryEditView(UpdateView):
    model = Gallery
    template_name = 'dashboard/gallery/edit.html'
    form_class = gallery_form.GalleryEditForm

    def get_success_url(self):
            return reverse('dashboard:gallery-list', kwargs={})

    def get_context_data(self, **kwargs):
        context = super(GalleryEditView, self).get_context_data(**kwargs)
        context['active_nav'] = 'gallery'
        if self.request.POST:
            context['gallery_images'] = gallery_form.GalleryImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['gallery_images'] = gallery_form.GalleryImageFormSet(
                instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        gallery_images = context['gallery_images']
        with transaction.atomic():
            self.object = form.save()
            if gallery_images.is_valid():
                gallery_images.instance = self.object
                gallery_images.save()
        return super(GalleryEditView, self).form_valid(form)


@method_decorator([login_required, admin_required], name='dispatch')
class GalleryDeleteView(DeleteView):
    model = Gallery
    success_url = reverse_lazy('dashboard:gallery-list')
