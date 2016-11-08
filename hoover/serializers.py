from rest_framework import serializers
from hoover.models import Hoover, Review


class HooverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hoover
        fields = ('id', 'nvmid', 'name', 'price', 'avg_rating')
