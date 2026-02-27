from rest_framework import serializers
from django.db.models import Avg
from .models import Course, Category, Lesson


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    #  calculate average rating
    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else 0

    # count reviews
    def get_total_reviews(self, obj):
        return obj.reviews.count()