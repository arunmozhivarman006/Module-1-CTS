# extensions.py — the SQLAlchemy instance lives here, not in app.py.
# Why this file exists: if `db = SQLAlchemy()` is defined inside app.py and
# you run `python app.py` directly, Python executes app.py as `__main__`.
# Any other file that then does `from app import db` re-imports app.py as a
# SEPARATE module named "app", creating a second, uninitialized SQLAlchemy
# instance — causing "the current Flask app is not registered with this
# SQLAlchemy instance" at request time. Defining `db` in its own module
# that everyone imports avoids the double-import entirely.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
