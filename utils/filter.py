import django_filters
from django_filters.rest_framework import FilterSet
from manager.models.api import Api
from manager.models.case import TestCase
from manager.models.plan import Plan
from manager.models.report import Report

"""
搜索相关类
"""

class ApiFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Api
        fields = ['name']


class TestCaseFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = TestCase
        fields = ['name','project']


class PlanFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    create_time = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Plan
        fields = ['name','create_time','project']


class ReportFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Report
        fields = ['name','plan','case']