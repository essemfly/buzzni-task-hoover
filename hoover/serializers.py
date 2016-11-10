from rest_framework import serializers
from hoover.models import Hoover, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'rating')


class HooverSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True, source='get_review')

    class Meta:
        model = Hoover
        fields = ('id', 'nvmid', 'name', 'price', 'avg_rating', 'review')
