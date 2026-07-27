# notes.py — HO1 Task 1: Request-Response Cycle, Middleware, WSGI/ASGI, MVT

# 1. GET /api/courses/ journey:
#    Browser -> WSGI/ASGI server -> Django URL router (urls.py, matches path)
#    -> View function/class (courses/views.py) -> Model layer runs ORM query
#    against the DB -> View builds a Response -> sent back through
#    middleware -> WSGI/ASGI server -> Browser.

# 2. Middleware sits between the server and the view, and again between the
#    view and the response, forming a chain both requests and responses
#    pass through.
#    - SecurityMiddleware: adds security headers, enforces HTTPS redirects.
#    - AuthenticationMiddleware: attaches request.user based on the session.

# 3. WSGI (Web Server Gateway Interface) is synchronous: one thread/process
#    handles one request at a time until it returns a response. ASGI
#    (Asynchronous Server Gateway Interface) supports async/await, so a
#    single process can juggle many concurrent I/O-bound requests
#    (websockets, long-lived connections, async views).
#    Django uses WSGI by default (wsgi.py). Switch to ASGI (asgi.py) when
#    you need websockets, async views, or long-polling.

# 4. MVC -> Django's MVT:
#    Model      -> Model      (same: data + DB schema)
#    Controller -> View       (Django's "View" holds the request-handling logic)
#    View       -> Template   (Django's "Template" renders the HTML/output)
