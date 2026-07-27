# wsgi.py — role: synchronous entry point used by traditional WSGI servers (gunicorn, uwsgi)
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coursemanager.settings")
application = get_wsgi_application()
