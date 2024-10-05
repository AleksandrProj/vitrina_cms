from typing import Any
from django import forms
from django.core.exceptions import ValidationError

from mailing.models import Subscribers


class SubscribersForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Ваше Имя"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Ваш E-mail"}))
    agreement = forms.BooleanField(error_messages={'required': "test"}, required=True)

    def clean_email(self):
        email_field = self.cleaned_data['email']
        subscribers = Subscribers.objects.filter(email=email_field)
        
        if subscribers.count() > 0:
            raise ValidationError("Такой email уже есть")
        return email_field

    class Meta:
        model = Subscribers
        fields = ('name', 'email', 'agreement')
        labels = {'name': 'Ваше имя', 'email': 'Ваш E-mail'}
