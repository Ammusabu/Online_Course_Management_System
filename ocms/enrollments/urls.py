from django.urls import path
from .views import enroll_course_page, complete_lesson_page, generate_certificate

urlpatterns = [
    path('enroll/<int:course_id>/', enroll_course_page, name='enroll_course'),
    path('complete/<int:lesson_id>/', complete_lesson_page, name='complete_lesson'),
    path('certificate/<int:course_id>/', generate_certificate, name='certificate'),
]