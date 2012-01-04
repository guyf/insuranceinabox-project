# Bring in the base settings (then override with live settings)
from settings import *

import logging
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s %(message)s',
)
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'iab_db', # Or path to database file if using sqlite3.
        'USER': 'iab',                      # Not used with sqlite3.
        'PASSWORD': 'ia4bbb',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

DOMAIN_ROOT_URL = 'http://iab.com'

FACEBOOK_APP_ID = '321784011167930'
FACEBOOK_APP_SECRET = '693a3596f86b003a26f9879d71d99afe'
FACEBOOK_API_KEY = '321784011167930'
FACEBOOK_APP_NAME = 'insurance-in-a-box-d'

#Registration settings
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
