# urls.py — role: the project's top-level URL table; delegates to app urls.py via include()
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("courses.urls")),
]
