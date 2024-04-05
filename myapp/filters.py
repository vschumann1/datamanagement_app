import django_filters
from .models import GSL_grouped_ISK_2022
from django.forms import CharField, TextInput

class ListCharFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value not in (None, '', 'alle'):  # 'alle' acts as a bypass keyword
            values = [v.strip() for v in value.split(',')]
            return qs.filter(**{f'{self.field_name}__in': values})
        return qs

class GSLFilter(django_filters.FilterSet):
    STR_NR = ListCharFilter(field_name='STR_NR', lookup_expr='in', label='Streckennummer:', widget=TextInput(attrs={'placeholder': '4010'}))

    def __init__(self, *args, **kwargs):
        super(GSLFilter, self).__init__(*args, **kwargs)
        if not self.data.get('STR_NR'):
            self.queryset = self.queryset.filter(STR_NR__in=['4010'])

    class Meta:
        model = GSL_grouped_ISK_2022
        fields = ['STR_NR']
