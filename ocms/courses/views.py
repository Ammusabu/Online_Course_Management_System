from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Lesson
from .serializers import CourseSerializer
from enrollments.models import Enrollment, LessonProgress
from reviews.models import Review


@api_view(['GET'])
def course_list(request):
    courses = Course.objects.filter(is_published=True)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk, is_published=True)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    serializer = CourseSerializer(course)
    return Response(serializer.data)


def home(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, 'home.html', {'courses': courses})


def course_detail_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')

    progress = 0
    enrolled = False
    completed_lessons = []

    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()

        if enrollment:
            enrolled = True

            total_lessons = lessons.count()
            completed = LessonProgress.objects.filter(
                enrollment=enrollment,
                completed=True
            ).count()

            if total_lessons > 0:
                progress = int((completed / total_lessons) * 100)

            completed_lessons = LessonProgress.objects.filter(
                enrollment=enrollment,
                completed=True
            ).values_list('lesson_id', flat=True)

    course_reviews = Review.objects.filter(course=course).select_related('student')

    return render(request, 'course_detail.html', {
    'course': course,
    'lessons': lessons,
    'progress': progress,
    'enrolled': enrolled,
    'completed_lessons': completed_lessons,
    'course_reviews': course_reviews
})