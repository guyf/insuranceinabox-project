from django import forms
from django.forms import ModelForm, TextInput, Field
from django.forms.models import modelformset_factory,inlineformset_factory
from django.contrib.auth.models import User
from commercialvehicle.models import *


class RiskForm(ModelForm):
    class Meta:
        model = Risk
        exclude = ('user')
        
class CommercialDriverForm(ModelForm):
    class Meta:
        model = CommercialDriver
        exclude = ('user','md_risk','ad_risk')
        widgets = {'dob': TextInput(attrs={'class': 'dobpicker'})}

class VehicleAddressForm(ModelForm):
    class Meta:
        model = VehicleAddress
        exclude = ('vehicle', 'geocoded_address')
        
class PolicyForm(ModelForm):
    class Meta:
        model = Policy

class ClaimForm(ModelForm):
    class Meta:
        model = Claim
        widgets = {'date': TextInput(attrs={'class': 'claimpicker', 'placeholder': 'claim date'})}

ClaimFormSet = modelformset_factory(Claim, form=ClaimForm, extra=3)          
ClaimInlineFormSet = inlineformset_factory(CommercialDriver, Claim, form=ClaimForm, extra=3)        
        

class ConvictionForm(ModelForm):
    class Meta:
        model = Conviction
        widgets = {'date': TextInput(attrs={'class': 'convpicker', 'placeholder': 'conviction date'})}

ConvictionFormSet = modelformset_factory(Conviction, form=ConvictionForm, extra=3)
ConvictionInlineFormSet = inlineformset_factory(CommercialDriver, Conviction, form=ConvictionForm, extra=3)  


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        exclude = ('risk')
        widgets = {'value': TextInput(attrs={'class': 'currency'}),}
        