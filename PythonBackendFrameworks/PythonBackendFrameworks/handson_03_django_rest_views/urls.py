# urls.py — copy into courses/urls.py, replacing the HO1 version
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("courses", views.CourseViewSet)
router.register("students", views.StudentViewSet)
router.register("enrollments", views.EnrollmentViewSet)

urlpatterns = [
    path("hello/", views.hello_view, name="hello"),
    path("", include(router.urls)),
]
# Router auto-generates:
#   GET/POST               /api/courses/
#   GET/PUT/PATCH/DELETE    /api/courses/{pk}/
#   GET                     /api/courses/{pk}/students/   <- custom @action
#   same pattern for students/ and enrollments/
