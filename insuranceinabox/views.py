import logging, urllib, urllib2
from django.conf import settings
from django.contrib import messages
#from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import redirect_to
from commercialvehicle.models import Risk, VehicleAddress
from familyincomebenefit.models import FIBRisk
from easy_maps.models import Address


def home(request):
    if request.user.is_authenticated():
        return welcome(request)
        
    return render_to_response('home.html', context_instance=RequestContext(request))
    

@login_required
def welcome(request):
    ''' list all the quotes the customer has all the products they cold get quotes on '''
    
    cvrs = Risk.objects.all().filter(user=request.user)
    fibrs = FIBRisk.objects.all().filter(user=request.user)
    
    return render_to_response('welcome.html', {'cv_risks':cvrs, 'fib_risks':fibrs}, context_instance=RequestContext(request))
    
    
@csrf_exempt
#@facebook_required
def fbapphome(request):
    
    '''
        facebook app canvas. Potentially comes throught this view twice
        1. If the user does not have the app installed request is a valid signed request
           with no 'code' on the url and we have no app permissions and so no access_token.
           So setup oauth_url and pass it to the template to redirect to with js (not ideal).
        2. User has accepted app install permissions request, fb redirect to the
           redirect_uri (back here) now with a code on the url. Call test_permissions
           and get_persistant_graph to convert this code into an access_token. Then
           call connect_user to create and/or log them in.
    '''
    
    logging.debug('RM: fbapphome request %s' % (request))    
    oauth_url = None
    
    verification_code = request.GET.get('code', None)
    logging.debug('RM: fbapphome verification_code %s' % (verification_code))


    #set up the permission required oauth_url and redirect uri, ideally shouldn't do this
    #every tme through but get_oauth_url returns both urls and adds attempt=1 to redirect_uri
    scope_list = settings.FACEBOOK_DEFAULT_SCOPE
    redirect_uri = 'http://apps.facebook.com/' + settings.FACEBOOK_APP_NAME + '/?facebook_login=1'
    from django_facebook.utils import get_oauth_url
    oauth_url, redirect_uri = get_oauth_url(request, scope_list, redirect_uri=redirect_uri)
    logging.debug('IAB: redirect_uri %s' % (redirect_uri))
    
    #useful to test that access_token is being retrieved
    #if verification_code:
    #    parms_dict = QueryDict('', True)
    #    parms_dict['client_id'] = settings.FACEBOOK_APP_ID
    #    parms_dict['client_secret'] = settings.FACEBOOK_APP_SECRET
    #    parms_dict['redirect_uri'] = redirect_uri  
    #    parms_dict['code'] = verification_code
    #    url = 'https://graph.facebook.com/oauth/access_token?'
    #    url += parms_dict.urlencode()
    #    logging.debug('RM: access_token URL: %s' % url)
    #    access_token = urllib2.urlopen(url).read()
    #    logging.debug('RM: fbapphome access_token %s' % (access_token))

    #test for permissions if we have them the user has authorised the app so set them up as a django user
    from django_facebook.utils import test_permissions
    if test_permissions(request, scope_list, redirect_uri):
        oauth_url = None #sadly have to reset this because it is set everytime through by get_oauth_url
        logging.debug('IAB: found required facebook permissions.')
        from django_facebook.api import get_persistent_graph, FacebookUserConverter
        graph = get_persistent_graph(request=request, redirect_uri=redirect_uri)
        facebook = FacebookUserConverter(graph)
        if facebook.is_authenticated():
            facebook_data = facebook.facebook_profile_data()
            from django_facebook.connect import connect_user
            #either, login register or connect the user
            action, user = connect_user(request)
            logging.debug('IAB: fbapphome user returned %s  with action %s' % (user, action))
        else:
            #TODO: handle this situation
            logging.error('IAB: fbapphome failed to authenticate the user from request: %s' % (request))
    else: #no permissions so construct oauth url and redirect to it in the template
        logging.debug('IAB: no app permissions so setting up oauth_url: %s.' % oauth_url)

    return render_to_response('welcome.html', {'oauth_url': oauth_url}, context_instance=RequestContext(request))


def map(request):
    mkrs = Address.objects.all()
    return render_to_response('cust_map.html', {'markers':mkrs,'width':'660', 'height':'500'}, context_instance=RequestContext(request))