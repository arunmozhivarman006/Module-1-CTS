# views.py — copy into courses/views.py (replaces the HO1 views.py)
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course, Student, Enrollment
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer


def hello_view(request):
    return HttpResponse("Course Management API is running")


# --- Task 1 (steps 27-28): plain APIView versions, kept for reference ---
class CourseListView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        return Response(CourseSerializer(courses, many=True).data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    def get_object(self, pk):
        return Course.objects.filter(pk=pk).first()

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CourseSerializer(course).data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Task 2 (steps 31-34): ViewSets replace the above — this is what urls.py wires up ---
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        student_ids = Enrollment.objects.filter(course_id=pk).values_list("student_id", flat=True)
        students = Student.objects.filter(id__in=student_ids)
        return Response(StudentSerializer(students, many=True).data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
