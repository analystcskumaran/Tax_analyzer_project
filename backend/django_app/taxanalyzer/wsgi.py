import os
from django.core.wsgi import get_wsgi_application

# Ensure Django knows which settings file to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxanalyzer.settings')

# This is the WSGI entry point Django expects
application = get_wsgi_application()
