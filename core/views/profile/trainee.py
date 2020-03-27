from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from core.decorators import trainee_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cards.models import Card
from cards.forms import ExtendCardRequestForm
from django.contrib import messages


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


@method_decorator([login_required, trainee_required], name='dispatch')
class TraineeCardExtendView(View):
    template_name = 'profile/trainees/cards/card_extend.html'

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
                return redirect( reverse('core:profile-trainee-cards-detail', args={card.pk}) + '?focus=collapseCardExtendRequest')

        context = {
            'card': card,
            'form': form,
            'sidebar_profile': 'cards'
        }
        return render(request, self.template_name, context=context)
