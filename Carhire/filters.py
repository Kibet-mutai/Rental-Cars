import django_filters

from .models import Car



class CarFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    city__name = django_filters.CharFilter(field_name = 'city', lookup_expr='icontains')
    rates_per_day__gt = django_filters.NumberFilter(field_name='rates_per_day', lookup_expr='gt')
    rates_per_day__lt = django_filters.NumberFilter(field_name='rates_per_day', lookup_expr='lt')



    class Meta:
        model = Car
        fields = ['name', 'city', 'capacity', 'rates_per_day']
