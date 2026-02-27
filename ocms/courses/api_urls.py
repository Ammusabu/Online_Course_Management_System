from django.urls import path
from .views import course_list, course_detail

urlpatterns = [
    path('', course_list, name='api_course_list'),
    path('<int:pk>/', course_detail, name='api_course_detail'),
]