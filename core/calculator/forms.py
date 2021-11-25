from django import forms
from .models import Methods
from .utils import available_operations, wrap_available_operations


def get_choices():
    ch = [(elem.name, elem.name) for elem in Methods.objects.all()]
    return ch


class OperationForm(forms.Form):
    choices = Methods.objects.all()
    ch = [(elem.name, elem.name) for elem in Methods.objects.all()]
    operation = forms.ChoiceField(choices=get_choices)
    params = forms.JSONField()


class AddOperationForm(forms.Form):
    out = wrap_available_operations()
    ch = []
    for i in out:
        ch.append((i, i))
    operation = forms.ChoiceField(choices=ch)