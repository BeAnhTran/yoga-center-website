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
from apps.make_up_lessons.models import MakeUpLesson
from apps.roll_calls.models import RollCall
from django.conf import settings
from django.utils.formats import date_format
from apps.absence_applications.models import AbsenceApplication
from apps.refunds.models import Refund, PENDING_STATE, APPROVED_STATE
from apps.card_types.models import FOR_TRAINING_COURSE


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
        context['number_of_expire_days_for_lessons'] = settings.NUMBER_OF_EXPIRE_DAYS_FOR_LESSON
        context ['FOR_TRAINING_COURSE'] = FOR_TRAINING_COURSE
        charged_str = card.get_payment_status()
        card_str_qrcode = '''Tên: {fname}\nEmail: {femail}\nMã số thẻ: {fcard_id}\nTên lớp: {fclass_name}\nLoại thẻ: {fcard_type}\nNgày bắt đầu: {fstart_at}\nNgày kết thúc: {fend_at}\nTrạng thái: {fis_charged}'''.format(
            fname=card.trainee.user.full_name(),
            femail=card.trainee.user.email,
            fcard_id=card.pk,
            fclass_name=card.yogaclass.name,
            fcard_type=card.card_type.name,
            fstart_at=date_format(
                card.start_at(), format='SHORT_DATE_FORMAT', use_l10n=True),
            fend_at=date_format(
                card.end_at(), format='SHORT_DATE_FORMAT', use_l10n=True),
            fis_charged=charged_str
        )
        if card.card_type.form_of_using == FOR_TRAINING_COURSE:
            if card.yogaclass.payment_periods.all().count() > 0:
                total_paid_amount = 0
                paid_payment_periods = []
                for invoice in card.invoices.all():
                    total_paid_amount += invoice.amount
                    if invoice.payment_period is not None:
                        paid_payment_periods.append(invoice.payment_period.pk)
                price_of_training_course = card.yogaclass.get_price_for_training_course()
                if total_paid_amount < price_of_training_course:
                    context['paid_entire'] = False
                else:
                    context['paid_entire'] = True
                unpaid_payment_periods = card.yogaclass.payment_periods.exclude(
                    pk__in=paid_payment_periods)
                context['unpaid_payment_periods'] = unpaid_payment_periods
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
        absence_applications = AbsenceApplication.objects.filter(
            roll_call__card__trainee=request.user.trainee)
        roll_calls = RollCall.objects.filter(**filter_options).exclude(refunds__state__in=[
            PENDING_STATE, APPROVED_STATE]).filter(id__in=[elem.roll_call.id for elem in absence_applications]).exclude(id__in=[elem.roll_call.id for elem in make_up_lessons_of_trainee]).distinct()
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
        context['roll_calls'] = roll_calls
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
