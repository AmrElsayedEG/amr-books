from django_filters import rest_framework as filters
from datetime import datetime

class BookFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name="active")
    author_name = filters.CharFilter(field_name="author_name")
    overdue = filters.BooleanFilter(method="filter_overdue")

    def filter_overdue(self, qs, name, value):
        if value:
            qs.filter(returned=False, return_date__lt = datetime.now())

class BorrowFilter(filters.FilterSet):
    returned = filters.BooleanFilter(field_name="returned")
    overdue = filters.BooleanFilter(method="filter_overdue")

    def filter_overdue(self, qs, name, value):
        if value:
            return qs.filter(returned=False, return_date__gt = datetime.now())
        return qs.filter(return_date__lt = datetime.now())