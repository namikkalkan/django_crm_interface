from .models import *
import django_filters
from django_filters import DateFilter,CharFilter

class OrderFilter (django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='from')
    end_date = DateFilter(field_name='date_created', lookup_expr='until')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = {'customer','date_created'}





#charfilter is for normal search - I can bring the info from order.product as well
#because there is fk relation