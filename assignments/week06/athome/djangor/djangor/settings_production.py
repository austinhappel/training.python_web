# Django settings for djangor project.
from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS
STATIC_ROOT = '/var/www/sites/week06-djangor/webroot/static'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'week06',                      # Or path to database file if using sqlite3.
        'USER': 'week06',                      # Not used with sqlite3.
        'PASSWORD': 'week06',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
