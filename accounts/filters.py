import django_filters
from django_filters import DateFilter, CharFilter
from .models import Order


class OrderFilter(django_filters.FilterSet):
    startDate = DateFilter(field_name='dateCreated', lookup_expr='gte')
    endDate = DateFilter(field_name='dateCreated', lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'dateCreated']
