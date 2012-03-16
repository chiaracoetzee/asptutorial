import sys, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trainingdemo.settings")
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__) + '/asp')
sys.path.append(os.path.dirname(__file__) + '/codepy')
sys.path.append(os.path.dirname(__file__) + '/cgen')

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
