import os, sys

sys.path.append(os.path.split(__file__)[0])

os.environ['DJANGO_SETTINGS_MODULE'] = 'opus_rest.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
