from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from familyincomebenefit.views import *

urlpatterns = patterns('',
#    url(r'^cloneprofile/select/$', fib_selectprofile, name='fib_selectprofile'),
#    url(r'^cloneprofile/(?P<profile_id>\d+)/$', fib_cloneprofile, name='fib_cloneprofile'),
    url(r'^risks/new/$', fib_createrisk, name='fib_createrisk'),
    url(r'^risks/(?P<risk_id>\d+)/$', fib_updaterisk, name='fib_updaterisk'),
    url(r'^risks/(?P<risk_id>\d+)/quote/new/$', fib_createquote, name='fib_createquote'),
#    url(r'^cvpremium/(?P<user_id>\d+)/$', personaldetails, name='personaldetails'),
#    url(r'^cvpayment/(?P<user_id>\d+)/$', drivinghistory, name='drivinghistory'),
)

