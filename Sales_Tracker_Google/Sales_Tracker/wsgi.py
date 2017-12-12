"""
WSGI config for Sales_Tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

import sys

sys.path.append("/home/user/CINS465-Project/Sales_Tracker_Google")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sales_Tracker.settings")

application = get_wsgi_application()
