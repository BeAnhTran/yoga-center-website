from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from apps.accounts.decorators import trainee_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.cards.models import Card
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.http import Http404
from apps.refunds.forms import RefundForm
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.db.models import CharField
from apps.refunds.models import Refund, PENDING_STATE
from apps.make_up_lessons.models import MakeUpLesson
from apps.roll_calls.models import RollCall
from django.conf import settings


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
        context['expire_month_of_lessons'] = settings.EXPIRE_MONTH_OF_LESSON
        card_str_qrcode = '''Tên: {fname}\nEmail: {femail}\nMã số thẻ: {fcard_id}\nTên lớp: {fclass_name}\nLoại thẻ: {fcard_type}\nNgày bắt đầu: {fstart_at}\nNgày kết thúc: {fend_at}'''.format(
            fname=card.trainee.user.full_name(),
            femail=card.trainee.user.email,
            fcard_id=card.pk,
            fclass_name=card.yogaclass.name,
            fcard_type=card.card_type.name,
            fstart_at=str(card.start_at()),
            fend_at=str(card.end_at())
        )

        context['card_str_qrcode'] = card_str_qrcode
        if request.GET.get('focus'):
            context['focus'] = request.GET.get('focus')
        return render(request, self.template_name, context=context)


# REFUND
@method_decorator([login_required, trainee_required], name='dispatch')
class RefundNewView(View):
    template_name = 'profile/trainees/cards/refunds/new.html'

    def get(self, request, pk):
        card = get_object_or_404(Card, pk=pk)
        for r in card.refunds.all():
            if r.state == PENDING_STATE:
                messages.error(
                    self.request, 'Bạn đang có yêu cầu đang chờ xử lý, vui lòng thử lại sau')
                return redirect(reverse('profile:profile-trainee-cards-detail', args={card.pk}) + '?focus=collapseCardRefundRequest')
        filter_options = {
            'studied': False,
            'card': card
        }
        make_up_lessons_of_trainee = MakeUpLesson.objects.filter(
            roll_call__card=card)
        query_choices = list()
        roll_calls = RollCall.objects.filter(**filter_options).exclude(
            id__in=[elem.roll_call.id for elem in make_up_lessons_of_trainee]).distinct()
        for r in roll_calls:
            query_choices += ((r.pk, r.lesson.str_without_class()),)
        form = RefundForm(
            initial={
                'unstudied_lessons': query_choices
            }
        )
        form.fields['card'].initial = card
        context = {}
        context['card'] = card
        context['form'] = form
        context['sidebar_profile'] = 'cards'
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        card = get_object_or_404(Card, pk=pk)
        filter_options = {
            'studied': False,
            'card': card
        }
        make_up_lessons_of_trainee = MakeUpLesson.objects.filter(
            roll_call__card=card)
        query_choices = list()
        roll_calls = RollCall.objects.filter(**filter_options).exclude(
            id__in=[elem.roll_call.id for elem in make_up_lessons_of_trainee]).distinct()
        for r in roll_calls:
            query_choices += ((r.pk, r.lesson.str_without_class()),)
        form = RefundForm(
            request.POST, request.FILES,
            initial={
                'unstudied_lessons': query_choices
            }
        )
        if form.is_valid():
            with transaction.atomic():
                form.save()
                messages.success(request, _(
                    'Create refund card request successfully'))
                return redirect(reverse('profile:profile-trainee-cards-detail', args={card.pk}) + '?focus=collapseCardRefundRequest')

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


@login_required
@trainee_required
def detele_refund_request(request, card_id, pk):
    card = get_object_or_404(Card, pk=card_id)
    obj = get_object_or_404(Refund, pk=pk, card=card)
    obj.delete()
    messages.success(request, 'Xóa yêu cầu hoàn tiền thành công')
    return redirect(reverse('profile:profile-trainee-cards-detail', args={card.pk}) + '?focus=collapseCardRefundRequest')
