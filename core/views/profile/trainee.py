from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from core.decorators import trainee_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cards.models import Card, ExtendCardRequest
from cards.forms import ExtendCardRequestForm
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.http import Http404
from refunds.forms import RefundForm
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.db.models import CharField
from refunds.models import Refund


@method_decorator([login_required, trainee_required], name='dispatch')
class TraineeCardsView(View):
    template_name = 'profile/trainees/cards/list.html'

    def get(self, request):
        context = {}
        cards = request.user.trainee.cards.all()
        context['cards'] = cards
        context['sidebar_profile'] = 'cards'
        return render(request, self.template_name, context=context)


@method_decorator([login_required, trainee_required], name='dispatch')
class TraineeCardDetailView(View):
    template_name = 'profile/trainees/cards/detail.html'

    def get(self, request, pk):
        card = Card.objects.get(pk=pk)
        context = {}
        context['card'] = card
        context['sidebar_profile'] = 'cards'
        if request.GET.get('focus'):
            context['focus'] = request.GET.get('focus')
        return render(request, self.template_name, context=context)


# EXTEND CARD REQUEST
@method_decorator([login_required, trainee_required], name='dispatch')
class TraineeCardExtendView(View):
    template_name = 'profile/trainees/cards/card_extends/new.html'

    def get(self, request, pk):
        card = Card.objects.get(pk=pk)
        form = ExtendCardRequestForm()
        context = {}
        context['card'] = card
        context['form'] = form
        context['sidebar_profile'] = 'cards'
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        card = Card.objects.get(pk=pk)
        form = ExtendCardRequestForm(request.POST, request.FILES)

        if form.is_valid():
            with transaction.atomic():
                data = {
                    'new_expire_date': form.cleaned_data['new_expire_date'],
                    'reason': form.cleaned_data['reason']
                }
                card.extend_card_requests.create(**data)
                messages.success(request, _(
                    'Create extend card request successfully'))
                return redirect(reverse('core:profile-trainee-cards-detail', args={card.pk}) + '?focus=collapseCardExtendRequest')

        context = {
            'card': card,
            'form': form,
            'sidebar_profile': 'cards'
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, trainee_required], name='dispatch')
class ExtendCardRequestDetailView(DetailView):
    model = ExtendCardRequest
    template_name = 'profile/trainees/cards/card_extends/show.html'

    def get_object(self):
        card_id = self.kwargs['card_id']
        card = get_object_or_404(Card, pk=card_id)
        obj = get_object_or_404(
            ExtendCardRequest, pk=self.kwargs['pk'], card=card)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ExtendCardRequestDetailView,
                        self).get_context_data(**kwargs)
        context['sidebar_profile'] = 'cards'
        return context


@method_decorator([login_required, trainee_required], name='dispatch')
class ExtendCardRequestEditView(UpdateView):
    model = ExtendCardRequest
    template_name = 'profile/trainees/cards/card_extends/edit.html'
    form_class = ExtendCardRequestForm

    def get_success_url(self):
        messages.success(self.request, 'Cập nhật yêu cầu gia hạn thành công')
        return (reverse('core:profile-trainee-cards-detail', args={self.object.card.pk}) + '?focus=collapseCardExtendRequest')

    def get_context_data(self, **kwargs):
        context = super(ExtendCardRequestEditView,
                        self).get_context_data(**kwargs)
        context['sidebar_profile'] = 'cards'
        return context


@login_required
@trainee_required
def detele_extend_card_request(request, card_id, pk):
    card = get_object_or_404(Card, pk=card_id)
    obj = get_object_or_404(ExtendCardRequest, pk=pk, card=card)
    obj.delete()
    messages.success(request, 'Xóa yêu cầu gia hạn thành công')
    return redirect(reverse('core:profile-trainee-cards-detail', args={card.pk}) + '?focus=collapseCardExtendRequest')


# REFUND
@method_decorator([login_required, trainee_required], name='dispatch')
class RefundNewView(View):
    template_name = 'profile/trainees/cards/refunds/new.html'

    def get(self, request, pk):
        card = Card.objects.get(pk=pk)
        query_choices = list()
        for lesson in card.lessons.all():
            query_choices += ((lesson.pk, lesson),)
        form = RefundForm(
            initial={
                'registered_lessons': query_choices
            }
        )
        form.fields['card'].initial = card
        context = {}
        context['card'] = card
        context['form'] = form
        context['sidebar_profile'] = 'cards'
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        card = Card.objects.get(pk=pk)
        query_choices = list()
        for lesson in card.lessons.all():
            query_choices += ((lesson.pk, lesson),)
        form = RefundForm(
            request.POST, request.FILES,
            initial={
                'registered_lessons': query_choices
            }
        )
        if form.is_valid():
            with transaction.atomic():
                form.save()
                messages.success(request, _(
                    'Create refund card request successfully'))
                return redirect(reverse('core:profile-trainee-cards-detail', args={card.pk}) + '?focus=collapseCardRefundRequest')

        context = {
            'card': card,
            'form': form,
            'sidebar_profile': 'cards'
        }
        return render(request, self.template_name, context=context)


@method_decorator([login_required, trainee_required], name='dispatch')
class RefundDetailView(DetailView):
    model = Refund
    template_name = 'profile/trainees/cards/refunds/show.html'

    def get_object(self):
        card_id = self.kwargs['card_id']
        card = get_object_or_404(Card, pk=card_id)
        obj = get_object_or_404(
            Refund, pk=self.kwargs['pk'], card=card)
        return obj

    def get_context_data(self, **kwargs):
        context = super(RefundDetailView,
                        self).get_context_data(**kwargs)
        context['sidebar_profile'] = 'cards'
        return context


@method_decorator([login_required, trainee_required], name='dispatch')
class RefundEditView(UpdateView):
    model = Refund
    template_name = 'profile/trainees/cards/refunds/edit.html'
    form_class = RefundForm

    def get_success_url(self):
        messages.success(self.request, 'Cập nhật yêu cầu hoàn tiền thành công')
        return (reverse('core:profile-trainee-cards-detail', args={self.object.card.pk}) + '?focus=collapseCardRefundRequest')

    def get_context_data(self, **kwargs):
        context = super(RefundEditView,
                        self).get_context_data(**kwargs)
        context['sidebar_profile'] = 'cards'
        return context


@login_required
@trainee_required
def detele_refund_request(request, card_id, pk):
    card = get_object_or_404(Card, pk=card_id)
    obj = get_object_or_404(Refund, pk=pk, card=card)
    obj.delete()
    messages.success(request, 'Xóa yêu cầu hoàn tiền thành công')
    return redirect(reverse('core:profile-trainee-cards-detail', args={card.pk}) + '?focus=collapseCardRefundRequest')
