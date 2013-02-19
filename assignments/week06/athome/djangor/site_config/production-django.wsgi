import os, sys
import site

site.addsitedir('/var/www/sites/week06-djangor/env/lib/python2.6/site-packages')
site.addsitedir('/var/www/sites/week06-djangor/djangor')
# site.addsitedir('/var/www/sites/week06-djangor/webapp')

sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangor.settings_production'
os.environ['DJANGO_WEB_ROOT']        = '/var/www/sites/week06-djangor/webroot'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()