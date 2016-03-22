"""
WSGI config for final_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/final_project')
sys.path.append('/var/www/final_project/final_project')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_project.settings")

application = get_wsgi_application()
