from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from core.decorators import trainee_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cards.models import Card
from cards.forms import ExtendCardRequestForm


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
