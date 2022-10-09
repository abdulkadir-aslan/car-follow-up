from random import choices
from django.forms import ChoiceField
import django_filters
from django_filters import DateFilter,CharFilter,ChoiceFilter

from page.models import *


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="create_at",lookup_expr="gte")
    end_date = DateFilter(field_name="create_at",lookup_expr="lte")
    plate= CharFilter(field_name = "car__plate",lookup_expr="icontains")
    contry = ChoiceFilter(choices=CONTRY)
    class Meta:
        model = Fuell
        fields = [
            "contry",
            "car__vehicle_type",
            "car__possession",
            "car__department",
        ]
        exclude = ['customer','create_at ']