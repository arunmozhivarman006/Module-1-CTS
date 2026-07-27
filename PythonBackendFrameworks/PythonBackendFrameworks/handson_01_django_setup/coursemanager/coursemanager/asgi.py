# asgi.py — role: async entry point used by ASGI servers (uvicorn, daphne) for websockets/async views
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coursemanager.settings")
application = get_asgi_application()
