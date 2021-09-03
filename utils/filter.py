import django_filters
from django_filters.rest_framework import FilterSet
from manager.models.api import Api


class ApiFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Api
        fields = ['name']