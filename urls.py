from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from insuranceinabox.views import *
from emailregistration.forms import EmailAuthenticationForm

#dependancy app URLS
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('emailregistration.backends.registration.simple_urls')),
    url(r'^$', home, name='registration_complete'),
    url(r'^fbapphome/$', fbapphome, name='fbapphome'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login', kwargs={'template_name':'registration/login.html', 'authentication_form':EmailAuthenticationForm}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^$', home, name='iab_home'),
    url(r'^welcome/$', welcome, name='welcome'),
    url(r'^map/$', map, name='map'),
    (r'^facebook/', include('django_facebook.urls')), #facebook/connect
    (r'^commercialvehicle/', include('commercialvehicle.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )