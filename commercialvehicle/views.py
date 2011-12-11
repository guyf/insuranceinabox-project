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
from commercialvehicle.models import *
from commercialvehicle.forms import *
from easymode.tree.xml import xml
from django.core import serializers
from easy_maps.models import Address


@login_required
def selectprofile(request):
      
    if request.method == 'POST':     
        #clone a profile into a risk based on submit name and navigate to updaterisk
        messages.error(request, 'Forms cannot be posted to this url')

    else: #handle GET
        if ClusterProfile.objects.count():
            ps = ClusterProfile.objects.all()
        else: #shouldn't be here no profiles so goto createrisk
            return HttpResponseRedirect(reverse('cv_createrisk'))

    return render_to_response('commercialvehicle/profiles.html', {'profiles': ps}, context_instance=RequestContext(request))


def cloneprofile(request, profile_id):
      
    if request.method == 'POST':     
        #clone a profile into a risk based on submit name and navigate to updaterisk
        messages.error(request, 'Forms cannot be posted to this url')

    else: #handle GET
        p = get_object_or_404(ClusterProfile, pk=profile_id)
        #create a new risk
        r = Risk.objects.get(clusterprofile=p.id)
        logging.debug('IAB-CV: risk id found %s' % r.id)
        vs = r.vehicle_set.all()
        logging.debug('IAB-CV: vehicles found %s' % str(vs))
        md = r.maindriver
        logging.debug('IAB-CV: maindriver found %s' % str(md))
        r.id = None
        r.name = ''
        r.user = request.user
        r.save()
        logging.debug('IAB-CV: new risk id created %s' % r.id)
        for v in vs:
            logging.debug('IAB-CV: cloning vehicle %s' % str(v.id))
            v.id = None
            v.risk = r
            v.user = None
            v.save()
        md.id = None
        logging.debug('IAB-CV: risk id now %s' % r.id)
        md.md_risk = r
        md.save()
        
        
    return HttpResponseRedirect(reverse('cv_updaterisk', args=[r.id]))


@login_required
def createrisk(request):
        
    if request.method == 'POST':    
        r_form = RiskForm(request.POST)
        v_form = VehicleForm(request.POST)
        a_form = VehicleAddressForm(request.POST)
        md_form = CommercialDriverForm(request.POST)
        md_claims_formset = ClaimFormSet(request.POST)
        md_convs_formset = ConvictionFormSet(request.POST)
        
        #check that required forms are not empty
        if not v_form.has_changed() or not a_form.has_changed() or not md_form.has_changed():
            messages.error(request, 'You must provide complete details of both a vehicle and a driver.')
            
        #check all forms are valid 
        else:
            if (r_form.is_valid() and v_form.is_valid() and a_form.is_valid() and v_form.is_valid()
                and md_claims_formset.is_valid() and md_claims_formset.is_valid()):
             
                r = r_form.save(commit=False)
                r.user = request.user
                r.save()
            
                v = v_form.save(commit=False)
                v.risk = r
                v.save()
            
                a = a_form.save(commit=False)
                #TODO: check this for geocode error and return to form
                map, _ = Address.objects.get_or_create(address=a or '')
                a.geocoded_address = map
                a.vehicle = v
                a.save()

                md = md_form.save(commit=False)
                md.md_risk = r
                md.user = request.user
                md.save()

                md_claims = md_claims_formset.save(commit=False)
                for md_claim in md_claims:
                    md_claim.commercialdriver = md
                    md_claim.save()

                md_convs = md_convs_formset.save(commit=False)
                for md_conv in md_claims:
                    md_conv.commercialdriver = md
                    md_conv.save()

                #navigate based on name of submit button
                if 'nav_quote' in request.POST:
                    #call to rating engine
                    return createquote(request, r.id)
                if 'nav_driver' in request.POST:
                    logging.debug("IAB-CV: creating risk and redirecting to add additional driver to risk: %s" % (r.id))
                    return HttpResponseRedirect(reverse('cv_createdriver', args=[r.id]))
                if 'nav_save' in request.POST:
                    logging.debug("IAB-CV: creating risk and redirecting to update risk: %s" % (r.id))
                    return HttpResponseRedirect(reverse('iab_home'))

    else: #handle GET  
        r_form = RiskForm()       
        v_form = VehicleForm()
        a_form = VehicleAddressForm()
        md_form = CommercialDriverForm()
        md_claims_formset = ClaimFormSet()
        md_convs_formset = ConvictionFormSet()

    return render_to_response('commercialvehicle/riskdata_form.html', {'r_form': r_form, 'v_form': v_form, 'a_form': a_form, 'md_form': md_form, 
                                                                       'md_claims_formset': md_claims_formset, 'md_convs_formset': md_convs_formset },
                                                                        context_instance=RequestContext(request))
@login_required
def updaterisk(request, risk_id):

    r = get_object_or_404(Risk, pk=risk_id)
    v = get_object_or_404(Vehicle, risk=risk_id)
    md = get_object_or_404(CommercialDriver, md_risk=risk_id)
    

    if request.method == 'POST':
        try: a = VehicleAddress.objects.get(vehicle=v)
        except ObjectDoesNotExist:
            a_form = VehicleAddressForm(request.POST)
        else:
            a_form = VehicleAddressForm(request.POST, instance=a)
            
        r_form = RiskForm(request.POST, instance=r)
        v_form = VehicleForm(request.POST, instance=v)
        md_form = CommercialDriverForm(request.POST, instance=md)
        md_claims_formset = ClaimInlineFormSet(request.POST, instance=md)
        md_convs_formset = ConvictionInlineFormSet(request.POST, instance=md)

        if (r_form.is_valid() and v_form.is_valid() and a_form.is_valid() and v_form.is_valid()
            and md_claims_formset.is_valid() and md_claims_formset.is_valid()):

            r = r_form.save(commit=False)
            r.save()        

            v = v_form.save(commit=False)
            v.risk = r
            v.save()

            a = a_form.save(commit=False)
            a.vehicle = v
            a.save()

            md = md_form.save(commit=False)
            md.md_risk = r
            md.save()

            md_claims = md_claims_formset.save(commit=False)
            for md_claim in md_claims:
                md_claim.save()

            md_convs = md_convs_formset.save(commit=False)
            for md_conv in md_claims:
                md_conv.save()

            #navigate based on name of submit button
            if 'nav_quote' in request.POST:
                #call to rating engine
                return createquote(request, r.id)
            if 'nav_driver' in request.POST:
                logging.debug("IAB-CV: creating risk to add additional driver to risk: %s" % (r.id))
                return HttpResponseRedirect(reverse('cv_createdriver', args=[r.id]))
            if 'nav_save' in request.POST:
                logging.debug("IAB-CV: creating risk and redirecting to update risk: %s" % (r.id))
                return HttpResponseRedirect(reverse('iab_home'))

    else: #handle GET 
        logging.debug("IAB-CV: get riskdata for update to risk: %s, driver: %s, vehicle: %s" % (r, md, v))
        try: a = VehicleAddress.objects.get(vehicle=v)
        except ObjectDoesNotExist:
            a_form = VehicleAddressForm()
        else:
            a_form = VehicleAddressForm(instance=a)
        r_form = RiskForm(instance=r)
        v_form = VehicleForm(instance=v)
        md_form = CommercialDriverForm(instance=md)
        md_claims_formset = ClaimInlineFormSet(instance=md)
        #logging.debug('IAB-CV: claims query: %s' % (Claim.objects.all().filter(commercialdriver=md)))
        #logging.debug('IAB-CV: claims form: %s' % (md_claims_formset))
        md_convs_formset = ConvictionInlineFormSet(instance=md)

    ads = CommercialDriver.objects.all().filter(ad_risk=risk_id)

    return render_to_response('commercialvehicle/riskdata_form.html', {'risk_id': risk_id, 'drivers': ads,
                                                                       'r_form': r_form, 'v_form': v_form, 'a_form': a_form, 'md_form': md_form, 
                                                                       'md_claims_formset': md_claims_formset, 'md_convs_formset': md_convs_formset },
                                                                        context_instance=RequestContext(request))


@login_required
def createdriver(request, risk_id):
    
    r = get_object_or_404(Risk, pk=risk_id)
      
    if request.method == 'POST':
        ad_form = CommercialDriverForm(request.POST)
        ad_claims_formset = ClaimFormSet(request.POST)
        ad_convs_formset = ConvictionFormSet(request.POST)
        
        if not ad_form.has_changed():
            messages.error(request, 'You must provide details of a driver.')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

        else:
            if ad_form.is_valid() and ad_claims_formset.is_valid() and ad_convs_formset.is_valid():
                ad = ad_form.save(commit=False)
                ad.ad_risk = r
                ad.save()

                ad_claims = ad_claims_formset.save(commit=False)
                for ad_claim in ad_claims:
                    ad_claim.commercialdriver = ad
                    ad_claim.save()

                ad_convs = ad_convs_formset.save(commit=False)
                for ad_conv in ad_claims:
                    ad_conv.commercialdriver = ad
                    ad_conv.save()

                #navigate back to the cv risk form
                return HttpResponseRedirect(reverse('cv_updaterisk', args=[risk_id]))

    else: #handle GET        
        ad_form = CommercialDriverForm()
        ad_claims_formset = ClaimInlineFormSet()
        ad_convs_formset = ConvictionInlineFormSet()

    return render_to_response('commercialvehicle/driver_form.html', {'risk_id': risk_id, 'ad_form': ad_form, 
                                                                     'ad_claims_formset': ad_claims_formset, 'ad_convs_formset': ad_convs_formset },
                                                                      context_instance=RequestContext(request))


@login_required
def updatedriver(request, risk_id, driver_id):
    
    r = get_object_or_404(Risk, pk=risk_id)
    ad = get_object_or_404(CommercialDriver, pk=driver_id)
      
    if request.method == 'POST':     
        ad_form = CommercialDriverForm(request.POST, instance=ad)
        ad_claims_formset = ClaimInlineFormSet(request.POST, instance=ad)
        ad_convs_formset = ConvictionInlineFormSet(request.POST, instance=ad)

    
        if ad_form.is_valid() and ad_claims_formset.is_valid() and ad_convs_formset.is_valid():
            ad = ad_form.save(commit=False)
            ad.ad_risk = r
            ad.save()

            ad_claims = ad_claims_formset.save(commit=False)
            for ad_claim in ad_claims:
                ad_claim.commercialdriver = ad
                ad_claim.save()

            ad_convs = ad_convs_formset.save(commit=False)
            for ad_conv in ad_claims:
                ad_conv.commercialdriver = ad
                ad_conv.save()

            #navigate back to the cv risk form
            return HttpResponseRedirect(reverse('cv_updaterisk', args=[risk_id]))

    else: #handle GET  
        #ads = CommercialDriver.objects.all().filter(ad_risk=risk_id)
        ad_form = CommercialDriverForm(instance=ad)
        ad_claims_formset = ClaimInlineFormSet(instance=ad)
        ad_convs_formset = ConvictionInlineFormSet(instance=ad)

    return render_to_response('commercialvehicle/driver_form.html', {'risk_id': risk_id, 'ad_form': ad_form, 
                                                                     'ad_claims_formset': ad_claims_formset, 'ad_convs_formset': ad_convs_formset },
                                                                      context_instance=RequestContext(request))

@login_required
def createquote(request, risk_id):

    r = get_object_or_404(Risk, pk=risk_id)

    ratingxml = xml(r)
    #ratingjson = serializers.serialize('json', Risk.objects.all(), indent=4, relations={'vehicle':{'relations':('vehicleaddress')}, 'maindriver'})
    #ratingjson = serializers.serialize('json', Risk.objects.filter(pk=risk_id), indent=4, relations=('Vehicle', 'maindriver', 'Quote', 'Policy'))
        
    p_year = float(random.randint(50000, 99999))/100
    p_month = Decimal(float(p_year/12*1.05)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    return render_to_response('commercialvehicle/quote.html', {'ratingxml': ratingxml, 'yearly': p_year, 'monthly': p_month  }, context_instance=RequestContext(request))
    
    
    
    
    
                                                   