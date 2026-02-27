from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from courses.models import Course
from .models import Review
from .serializers import ReviewSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    course_id = request.data.get('course_id')
    rating = request.data.get('rating')
    comment = request.data.get('comment', '')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)

    # prevent duplicate review
    if Review.objects.filter(student=request.user, course=course).exists():
        return Response({'error': 'You already reviewed this course'})

    review = Review.objects.create(
        student=request.user,
        course=course,
        rating=rating,
        comment=comment
    )

    return Response(ReviewSerializer(review).data)
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from enrollments.models import Enrollment
from .models import Review

@login_required
def add_review_page(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    # user must be enrolled
    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    if not enrollment:
        return redirect('course_detail', course_id=course.id)

    if request.method == "POST":
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '')

        Review.objects.update_or_create(
            student=request.user,
            course=course,
            defaults={
                'rating': rating,
                'comment': comment
            }
        )

    return redirect('course_detail', course_id=course.id)