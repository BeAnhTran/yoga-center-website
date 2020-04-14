from django.shortcuts import render
from django.views import View

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator([login_required], name='dispatch')
class BillListView(View):
    template_name = 'profile/bills.html'

    def get(self, request):
        context = {}
        bills = request.user.bills.all()
        context = {
            'bills': bills,
            'sidebar_profile': 'bills'
        }
        return render(request, self.template_name, context=context)
