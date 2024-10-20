from django import forms

from mailing.models import Subscribers


class SubscribersForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Ваше Имя"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Ваш E-mail"}))
    agreement = forms.BooleanField(error_messages={'required': "test"}, required=True)

    class Meta:
        model = Subscribers
        fields = ('name', 'email', 'agreement')
        labels = {'name': 'Ваше имя', 'email': 'Ваш E-mail'}
