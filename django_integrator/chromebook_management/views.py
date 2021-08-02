from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from .forms.check_in import CheckInForm
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest


class CheckinView(FormView):
    template_name = 'check_in.html'
    form_class = CheckInForm
    success_url = '/check_in/'

    def form_valid(self, form):
        # request = WSGIRequest('POST')
        # messages.success(request, 'Successfully Checked in Serial Number!')
        # print('valid submission', self.cleaned_data['serial_number'], self.cleaned_data['manufacturing_model'])
        print('in valid form method')
        return super(CheckinView, self).form_valid(form)
        # def check_in(self):
        #     print(self.serial_number)
        #     print(self.manufacturing_model)
        #
        # def post(self, request: WSGIRequest) -> HttpResponseRedirect:
        #     if self.is_valid():
        #
        #     else:
        #         messages.error(request, 'Failure Checked in Serial Number!')
        #         print('invalid submission', self.cleaned_data['serial_number'])
        #         return HttpResponseRedirect('/chromebooks/check_in')


def index(request):
    return render(request, 'index.html')

