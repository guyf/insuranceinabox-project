from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from commercialvehicle.views import *

urlpatterns = patterns('',
    url(r'^cloneprofile/select/$', selectprofile, name='fib_selectprofile'),
    url(r'^cloneprofile/(?P<profile_id>\d+)/$', cloneprofile, name='fib_cloneprofile'),
    url(r'^risks/new/$', createrisk, name='fib_createrisk'),
    url(r'^risks/(?P<risk_id>\d+)/$', updaterisk, name='fib_updaterisk'),
    url(r'^risks/(?P<risk_id>\d+)/quote/new/$', createquote, name='fib_createquote'),
#    url(r'^cvpremium/(?P<user_id>\d+)/$', personaldetails, name='personaldetails'),
#    url(r'^cvpayment/(?P<user_id>\d+)/$', drivinghistory, name='drivinghistory'),
)

