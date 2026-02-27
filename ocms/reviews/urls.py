from django.urls import path
from .views import add_review_page

urlpatterns = [
    path('add/<int:course_id>/', add_review_page, name='add_review'),
]