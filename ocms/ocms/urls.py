from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # WEBSITE PAGES
    path('', include('courses.urls')),          # home + course pages
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('reviews/', include('reviews.urls')),

    # API (separate namespace)
    path('api/courses/', include('courses.api_urls')),
]