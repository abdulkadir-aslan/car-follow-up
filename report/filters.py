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
            "car__plate",
            "contry",
            "car__vehicle_type",
            "car__possession",
            "car__department",
        ]
        exclude = ['customer','create_at ']

class CarFilter(django_filters.FilterSet):
    plate= CharFilter(field_name = "plate",lookup_expr="icontains")
    contry = ChoiceFilter(choices=CONTRY)
    
    class Meta:
        model = Car
        fields = [
            "plate",
            "contry",
            "vehicle_type",
            "possession",
            "department",
            "status",
        ]
        exclude = ['customer','create_at ']
   
class LiterFilter(django_filters.FilterSet):
    plate= CharFilter(field_name = "car__plate",lookup_expr="icontains")
    contry = ChoiceFilter(choices=CONTRY)
    
    class Meta:
        model = Fuell
        fields = [
            "car__plate",
            "contry",
            "car__vehicle_type",
            "car__possession",
        ]
        exclude = ['customer','create_at ']
   
class PlateFilter(django_filters.FilterSet):
    plate= CharFilter(field_name = "plate",lookup_expr="icontains")
    class Meta:
        model = Car
        fields = [
            "plate",
             ]
        exclude = ['customer','create_at ']

class FuelPlateFilter(django_filters.FilterSet):
    plate= CharFilter(field_name = "car__plate",lookup_expr="icontains")
    class Meta:
        model = Fuell
        fields = [
            "car__plate",
             ]
        exclude = ['customer','create_at ']

class ChangeHistoryFilter(django_filters.FilterSet):
    user_name = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains', label='Kullanıcı Adı')
    change_type = django_filters.ChoiceFilter(choices=[('update', 'Düzenlendi'), ('create', 'Oluşturuldu'), ('delete', 'Silindi')], label='Durum', required=False)
    field_name = django_filters.CharFilter(field_name='field_name', lookup_expr='icontains', label='Değişen Kısım', required=False)
    plate_number = django_filters.CharFilter(field_name='old_value', lookup_expr='icontains', label='Plaka', required=False)

    class Meta:
        model = ChangeHistory
        fields = ['user_name', 'change_type', 'field_name', 'plate_number']  