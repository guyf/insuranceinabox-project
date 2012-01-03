from django import forms
from django.forms import ModelForm, TextInput, Field
from django.forms.models import modelformset_factory,inlineformset_factory
from django.contrib.auth.models import User
from familyincomebenefit.models import *


class FIBRiskForm(ModelForm):
    class Meta:
        model = FIBRisk
        exclude = ('user')


class LifeInsuredForm(ModelForm):
    class Meta:
        model = LifeInsured
        exclude = ('risk','user')
        