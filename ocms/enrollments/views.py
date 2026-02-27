from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reportlab.pdfgen import canvas
from django.utils.timezone import now

from courses.models import Course, Lesson
from .models import Enrollment, LessonProgress


# =========================================
# 🔹 HELPER FUNCTION
# =========================================

from .models import Enrollment, LessonProgress
from courses.models import Lesson

def calculate_progress(student, course):
    try:
        enrollment = Enrollment.objects.get(student=student, course=course)
    except Enrollment.DoesNotExist:
        return 0

    total_lessons = Lesson.objects.filter(course=course).count()

    if total_lessons == 0:
        return 0

    completed_lessons = LessonProgress.objects.filter(
        enrollment=enrollment,
        completed=True
    ).count()

    return int((completed_lessons / total_lessons) * 100)
# =========================================
# 🔹 API VIEWS (For DRF)
# =========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request):

    course_id = request.data.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    if not created:
        return Response({"message": "Already enrolled"})

    return Response({"message": "Enrolled successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses(request):

    enrollments = Enrollment.objects.filter(student=request.user)

    response_data = []

    for enrollment in enrollments:
        course = enrollment.course
        progress = calculate_progress(request.user, course)

        response_data.append({
            "course_id": course.id,
            "title": course.title,
            "progress": progress
        })

    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_lesson(request):

    lesson_id = request.data.get('lesson_id')

    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return Response({'error': 'Lesson not found'}, status=404)

    progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson
    )

    progress.completed = True
    progress.save()

    course = lesson.course
    percentage = calculate_progress(request.user, course)

    if percentage == 100:
        return Response({
            "message": "Lesson marked as completed",
            "course_status": "COURSE COMPLETED 🎓"
        })

    return Response({
        "message": "Lesson marked as completed",
        "progress": f"{percentage}%"
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_certificate(request, course_id):

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    progress = calculate_progress(request.user, course)

    if progress < 100:
        return Response({"error": "Course not completed yet"}, status=400)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{course_id}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(300, 750, "Certificate of Completion")

    p.setFont("Helvetica", 16)
    p.drawCentredString(300, 680, "This is to certify that")

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(300, 650, request.user.email)

    p.setFont("Helvetica", 16)
    p.drawCentredString(300, 600, "has successfully completed the course")

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(300, 560, course.title)

    p.setFont("Helvetica", 12)
    p.drawCentredString(300, 520, f"Date: {now().date()}")

    p.showPage()
    p.save()

    return response


# =========================================
# 🔹 HTML PAGE VIEWS (For Frontend)
# =========================================


# ---------- ENROLL PAGE ----------
@login_required
def enroll_course_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # prevent duplicate enrollment
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        Enrollment.objects.create(student=request.user, course=course)

    return redirect(f"/courses/{course.id}/")


# ---------- COMPLETE LESSON PAGE ----------
from django.utils.timezone import now

@login_required
def complete_lesson_page(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=lesson.course
    )

    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    progress.completed = True
    progress.completed_at = now()
    progress.save()

    return redirect('course_detail', course_id=lesson.course.id)


# ---------- DASHBOARD PAGE ----------
@login_required
def my_courses_page(request):
    enrollments = Enrollment.objects.filter(student=request.user)

    courses_data = []
    for enrollment in enrollments:
        course = enrollment.course
        progress = calculate_progress(request.user, course)

        courses_data.append({
            'course': course,
            'progress': progress
        })

    return render(request, 'my_courses.html', {'courses_data': courses_data})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Enrollment
from .views import calculate_progress


@login_required
def dashboard_view(request):
    enrollments = Enrollment.objects.filter(student=request.user)

    courses_data = []

    for enrollment in enrollments:
        course = enrollment.course
        progress = calculate_progress(request.user, course)

        courses_data.append({
            'course': course,
            'progress': progress
        })

    return render(request, 'dashboard.html', {'courses_data': courses_data})