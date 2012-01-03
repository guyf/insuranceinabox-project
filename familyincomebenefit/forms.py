from django import forms
from django.forms import ModelForm, TextInput, Field
from django.forms.models import modelformset_factory,inlineformset_factory
from django.contrib.auth.models import User
from familyincomebenefit.models import *


class RiskForm(ModelForm):
    class Meta:
        model = Risk
        exclude = ('user')


class InsuredLifeForm(ModelForm):
    class Meta:
        model = InsuredLife
        