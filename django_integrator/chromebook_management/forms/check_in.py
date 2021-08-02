from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CheckInForm(forms.Form):
    # @TODO pull models from db
    chrome_models = [('Dell 3100', 'Dell 3100'), ('Dell 3180', 'Dell 3180'), ('HP 11A', 'HP 11A')]

    serial_number = forms.CharField(
        label='Serial Number',
        max_length=50)
    manufacturing_model = forms.CharField(
        label='Chromebook Model',
        widget=forms.Select(choices=chrome_models))
    print_label = forms.BooleanField(
        label='Print Label',
        required=False)
    needs_unlock = forms.BooleanField(
        label='Needs Unlock',
        required=False)
    student_email = forms.CharField(
        label='Student UPrep email address',
        max_length=50,
        required=False)

    def __init__(self, *args, **kwargs):
        super(CheckInForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

