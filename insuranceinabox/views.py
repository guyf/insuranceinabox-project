import logging
from django.conf import settings
from django.contrib import messages
#from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from commercialvehicle.models import Risk, VehicleAddress
from easy_maps.models import Address


def home(request):
    if request.user.is_authenticated():
        return welcome(request)
        
    return render_to_response('home.html', context_instance=RequestContext(request))
    

@login_required
def welcome(request):
    ''' list all the quotes the customer has all the products they cold get quotes on '''
    
    rs = Risk.objects.all().filter(user=request.user)
    
    return render_to_response('welcome.html', {'risks':rs}, context_instance=RequestContext(request))
    
    
#def iab_register(request):
#    """
#    just a wrapper for the registration.register view
#    """
    #if it a post some error checking before passing on to registration
#    if request.method == 'POST':
#        user_form = RegisterUserForm(request.POST)
#        if user_form.is_valid():
#            return register(request, backend='insuranceinabox.backends.registration.SimpleBackend',  
#	 				                disallowed_url='registration_disallowed', success_url=reverse('registersuccess'),
#							        template_name='registration/invite_participant.html', form_class=IABRegistrationForm)
#        else:
#            logging.info("GM: Failed to register a new non-social network user.")
	        #TODO: find out why and tell them
#            messages.error(request, 'Your user was not added because: %s, if you think this error should not have occurred please let us know.' % str(user_form.errors))
#            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    #if a get just pass straight through
#    else:
#        return register(request, backend='insuranceinabox.backends.registration.SimpleBackend',  
#                disallowed_url='registration_disallowed', success_url=reverse('registersuccess'),
#                template_name='registration/register_user.html', form_class=IABRegistrationForm)


def map(request):
    mkrs = Address.objects.all()
    return render_to_response('cust_map.html', {'markers':mkrs,'width':'660', 'height':'500'}, context_instance=RequestContext(request))