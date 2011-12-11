import logging
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django_facebook.models import FacebookProfileModel

class UserProfile(FacebookProfileModel):
    user = models.OneToOneField(User)
    timezone = models.CharField(max_length=50, default='Europe/London', blank=True)
    notify_emails = models.BooleanField(default=False)
    news_emails = models.BooleanField(default=False)
    is_betatester = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        """Create the UserProfile when a new User is saved"""
        logging.debug("CREATING PROFILE1")
        if created:
            logging.debug("CREATING PROFILE1")
            profile = UserProfile()
            profile.user = instance
            profile.save()
    
    import logging;logging.debug("REGISTERING")
    post_save.connect(create_user_profile, sender=User)