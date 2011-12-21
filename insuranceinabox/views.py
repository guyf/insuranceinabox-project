import logging, urllib, urllib2
from django.conf import settings
from django.contrib import messages
#from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import redirect_to
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
    
    
@csrf_exempt
#@facebook_required
def fbapphome(request):

    oauth_url = None
    logging.debug('RM: fbapphome request %s' % (request))
    verification_code = request.GET.get('code', None)
    logging.debug('RM: fbapphome verification_code %s' % (verification_code))                           


    #set up the permission required and redirect uri
    scope_list = settings.FACEBOOK_DEFAULT_SCOPE
    redirect_uri = request.build_absolute_uri(request.path) + '?facebook_login=1'
    from django_facebook.utils import cleanup_oauth_url, get_oauth_url
    oauth_url, redirect_uri = get_oauth_url(request, scope_list, redirect_uri=redirect_uri)
    #redirect_uri = cleanup_oauth_url(redirect_uri)
    logging.debug('IAB: redirect_uri %s' % (redirect_uri))
    
    if verification_code:
        redirect_uri = urllib.quote(redirect_uri)
        url = str('https://graph.facebook.com/oauth/access_token?client_id='+ settings.FACEBOOK_APP_ID + 
                  '&client_secret='+ settings.FACEBOOK_APP_SECRET + '&redirect_uri=' + redirect_uri + '&code=' + verification_code)
        logging.debug('URL: %s' % url)
        access_token = urllib2.urlopen(url).read()
        logging.debug('RM: fbapphome access_token %s' % (access_token))

    #test for permissions if we have them the user has authorised the app
    #so set them up as a django user
    from django_facebook.utils import test_permissions
    if test_permissions(request, scope_list, redirect_uri):
        oauth = None
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
    #no permissions so construct oauth url and redirect to it in the template
    else:
        redirect_uri = urllib.quote(redirect_uri)
        oauth_url = 'https://www.facebook.com/dialog/oauth'
        logging.debug('IAB: no app permissions so setting up oauth_url: %s.' % oauth_url)
        kwargs = {'client_id':settings.FACEBOOK_APP_ID, 'redirect_uri':redirect_uri, 'scope':'email'}
        return redirect_to(request, oauth_url, **kwargs)

    return render_to_response('welcome.html', {'oauth_url': oauth_url}, context_instance=RequestContext(request))


def map(request):
    mkrs = Address.objects.all()
    return render_to_response('cust_map.html', {'markers':mkrs,'width':'660', 'height':'500'}, context_instance=RequestContext(request))