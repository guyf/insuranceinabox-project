from django.conf.urls.defaults import *
from emailregistration.forms import EmailRegistrationForm


urlpatterns = patterns('',
    url(r'^register/$', 'registration.views.register', {'backend':'emailregistration.backends.registration.DefaultEmailRegBackend','form_class': EmailRegistrationForm}, name='registration_register'),
    (r'', include('registration.backends.default.urls')),
)