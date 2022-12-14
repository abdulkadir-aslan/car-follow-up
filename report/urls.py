from django.urls import  path
from report.views import *

urlpatterns = [
    path('Genel_Raporlama',general_report,name="general_report"),
    path('Araç_bilgileri_Raporlama',car_about_report,name="car_about_report"),
    path('Lt_Km_Raporlama',lt_km_report,name="lt_km_report"),
    path('Plaka_Raporlama',plate_report,name="plate_report"),
    #export pdf,excel
    path('export_excel',export_Excel,name='export-excel'),
    path('export_liter_excel',export_Liter_Excel,name='export-liter-excel'),
    path('export_car_excel',export_Car_Excel,name='export-car-excel'),

]