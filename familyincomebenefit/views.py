import logging
import random
from decimal import *
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from familyincomebenefit.models import *
from familyincomebenefit.forms import *
from easymode.tree.xml import xml
from django.core import serializers
from easy_maps.models import Address


@login_required
def fib_selectprofile(request):
      
    if request.method == 'POST':     
        #clone a profile into a risk based on submit name and navigate to updaterisk
        messages.error(request, 'Forms cannot be posted to this url')

    else: #handle GET
        if ClusterProfile.objects.count():
            ps = ClusterProfile.objects.all()
        else: #shouldn't be here no profiles so goto createrisk
            return HttpResponseRedirect(reverse('fib_createrisk'))

    return render_to_response('familyincomebenefit/profiles.html', {'profiles': ps}, context_instance=RequestContext(request))


def fib_cloneprofile(request, profile_id):
      
    if request.method == 'POST':     
        #clone a profile into a risk based on submit name and navigate to updaterisk
        messages.error(request, 'Forms cannot be posted to this url')

    else: #handle GET
        p = get_object_or_404(ClusterProfile, pk=profile_id)
        #create a new risk
        r = FIBRisk.objects.get(clusterprofile=p.id)
        logging.debug('IAB-FIB: risk id found %s' % r.id)
        lis = r.lifeinsured_set.all()
        logging.debug('IAB-FIB: insuredlives found %s' % str(lis))
        r.id = None
        r.name = ''
        r.user = request.user
        r.save()
        logging.debug('IAB-FIB: new risk id created %s' % r.id)
        for li in lis:
            logging.debug('IAB-FIB: cloning insuredlife %s' % str(li.id))
            li.id = None
            li.risk = r
            li.user = None
            li.save()
        
    return HttpResponseRedirect(reverse('fib_updaterisk', args=[r.id]))


@login_required
def fib_createrisk(request):
        
    if request.method == 'POST':    
        r_form = FIBRiskForm(request.POST)
        li_form = LifeInsuredForm(request.POST)
        #a_form = AddressForm(request.POST)

        #check that required forms are not empty
        if not li_form.has_changed():
            messages.error(request, 'You must provide complete details of both a vehicle and a driver.')
            
        #check all forms are valid 
        else:
            if (r_form.is_valid() and li_form.is_valid()): #and a_form.is_valid()
             
                r = r_form.save(commit=False)
                r.user = request.user
                r.save()
                
                li = li_form.save(commit=False)
                li.risk = r
                li.save()
            
                #a = a_form.save(commit=False)
                #TODO: check this for geocode error and return to form
                #map, _ = Address.objects.get_or_create(address=a or '')
                #a.geocoded_address = map
                #a.vehicle = v
                #a.save()

                #navigate based on name of submit button
                if 'nav_quote' in request.POST:
                    #call to rating engine
                    return fib_createquote(request, r.id)
                if 'nav_save' in request.POST:
                    logging.debug("IAB-FIB: creating risk and redirecting to update risk: %s" % (r.id))
                    return HttpResponseRedirect(reverse('iab_home'))

    else: #handle GET  
        r_form = FIBRiskForm()
        li_form = LifeInsuredForm()
        logging.debug("IAB-FIB: li_form: %s" % str(li_form))   
        #a_form = VehicleAddressForm()

    return render_to_response('familyincomebenefit/riskdata_form.html', {'r_form': r_form, 'li_form': li_form }, context_instance=RequestContext(request))
    
    
@login_required
def fib_updaterisk(request, risk_id):

    r = get_object_or_404(FIBRisk, pk=risk_id)
    li = get_object_or_404(LifeInsured, risk=risk_id)

    if request.method == 'POST':
        #try: a = VehicleAddress.objects.get(vehicle=v)
        #except ObjectDoesNotExist:
        #    a_form = VehicleAddressForm(request.POST)
        #else:
        #    a_form = VehicleAddressForm(request.POST, instance=a)
            
        r_form = FIBRiskForm(request.POST, instance=r)
        li_form = LifeInsuredForm(request.POST, instance=li)

        if (r_form.is_valid() and li_form.is_valid()):

            r = r_form.save(commit=False)
            r.save()
            
            li = li_form.save(commit=False)
            li.risk = r
            li.save()    

            #navigate based on name of submit button
            if 'nav_quote' in request.POST:
                #call to rating engine
                return fib_createquote(request, r.id)
            if 'nav_save' in request.POST:
                logging.debug("IAB-FIB: creating risk and redirecting to update risk: %s" % (r.id))
                return HttpResponseRedirect(reverse('iab_home'))

    else: #handle GET 
        logging.debug("IAB-FIB: get riskdata for update to risk: %s" % (r))
        #try: a = VehicleAddress.objects.get(vehicle=v)
        #except ObjectDoesNotExist:
        #    a_form = VehicleAddressForm()
        #else:
        #    a_form = VehicleAddressForm(instance=a)
        r_form = FIBRiskForm(instance=r)
        li_form = LifeInsuredForm(instance=li) 

    return render_to_response('familyincomebenefit/riskdata_form.html', {'risk_id': risk_id, 'r_form': r_form, 'li_form': li_form }, context_instance=RequestContext(request))


@login_required
def fib_createquote(request, risk_id):

    r = get_object_or_404(FIBRisk, pk=risk_id)

    #ratingxml = xml(r)
    #ratingjson = serializers.serialize('json', Risk.objects.all(), indent=4, relations={'vehicle':{'relations':('vehicleaddress')}, 'maindriver'})
    #ratingjson = serializers.serialize('json', Risk.objects.filter(pk=risk_id), indent=4, relations=('Vehicle', 'maindriver', 'Quote', 'Policy'))
        
    p_year = float(random.randint(50000, 99999))/100
    p_month = Decimal(float(p_year/12*1.05)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    return render_to_response('familyincomebenefit/quote.html', {'yearly': p_year, 'monthly': p_month  }, context_instance=RequestContext(request))
    
                                                   