from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from enrollments.models import Enrollment
from enrollments.views import calculate_progress


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

    return render(request, 'dashboard.html', {
        'courses_data': courses_data
    })