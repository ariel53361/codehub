from django_filters import rest_framework as filters
from .models import Room


class RoomFilter(filters.FilterSet):
    topic = filters.NumberFilter(field_name="topic__id")
    subject = filters.CharFilter(field_name="subject", lookup_expr='icontains')

    class Meta:
        model = Room
        fields = ['topic', 'subject']
