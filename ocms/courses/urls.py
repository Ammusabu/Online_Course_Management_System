from django.urls import path
from .views import home, course_detail_page

urlpatterns = [
    path('', home, name='home'),
    path('courses/<int:course_id>/', course_detail_page, name='course_detail'),
]