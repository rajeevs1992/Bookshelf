import os
import sys
sys.path.append('/home/rajeevs/myFiles/projects/books')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
