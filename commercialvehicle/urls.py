from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from commercialvehicle.views import *

urlpatterns = patterns('',
    url(r'^cloneprofile/select/$', selectprofile, name='cv_selectprofile'),
    url(r'^cloneprofile/(?P<profile_id>\d+)/$', cloneprofile, name='cv_cloneprofile'),
    url(r'^risks/new/$', createrisk, name='cv_createrisk'),
    url(r'^risks/(?P<risk_id>\d+)/$', updaterisk, name='cv_updaterisk'),
    url(r'^risks/(?P<risk_id>\d+)/drivers/new/$', createdriver, name='cv_createdriver'),
    url(r'^risks/(?P<risk_id>\d+)/drivers/(?P<driver_id>\d+)/$', updatedriver, name='cv_updatedriver'),
    url(r'^risks/(?P<risk_id>\d+)/quote/new/$', createquote, name='cv_createquote'),
#    url(r'^cvpremium/(?P<user_id>\d+)/$', personaldetails, name='personaldetails'),
#    url(r'^cvpayment/(?P<user_id>\d+)/$', drivinghistory, name='drivinghistory'),
)

