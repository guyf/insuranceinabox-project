import logging
from django.contrib import messages
from django import template
from django.contrib.auth.models import User
from motorfleet.models import Vehicle, Claim
from motorfleet.forms import VehicleFormSet, ClaimFormSet
from exptracker.models import SharedExpense


register = template.Library()


@register.inclusion_tag('motorfleet/tag_edit_vehicles.html')
def edit_vehicles(sharedexpense, for_user):
    #TODO: validate there are legitimate paramters
    if isinstance(sharedexpense,SharedExpense):
        se = sharedexpense
    else:
        se = SharedExpense.objects.get(pk=sharedexpense)

    if isinstance(for_user,User):
        u = for_user
    else:
        u = User.objects.get(username=for_user)

    vehicle_formset = VehicleFormSet(queryset=Vehicle.objects.all().filter(owner=u), prefix=u.id)

    return {'sharedexpense':se, 'v_formset':vehicle_formset}


@register.inclusion_tag('motorfleet/tag_edit_claims.html')
def edit_claims(sharedexpense, for_user):
    #TODO: validate there are legitimate paramters
    if isinstance(sharedexpense,SharedExpense):
        se = sharedexpense
    else:
        se = SharedExpense.objects.get(pk=sharedexpense)

    if isinstance(for_user,User):
        u = for_user
    else:
        u = User.objects.get(username=for_user)

    claim_formset = ClaimFormSet(queryset=Claim.objects.all().filter(driver=u), prefix=u.id)

    return {'sharedexpense':se, 'c_formset':claim_formset}