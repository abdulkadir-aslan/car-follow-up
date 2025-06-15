from django.shortcuts import render
from page.models import Car,Fuell
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from page.decorators import *
from datetime import datetime,date
from calendar import monthrange
from django.db.models import Sum
from django.core.paginator import Paginator
from .filters import OrderFilter,CarFilter,LiterFilter

import xlwt
from django.http import HttpResponse


@login_required(login_url="login")
@employe_only
def general_report(request):
    fuel = Fuell.objects.select_related("car", "user").all().order_by('-create_at')
    myFilter = OrderFilter(request.GET, queryset=fuel)
    fuel = myFilter.qs

    paginator = Paginator(fuel, 10)  # Sayfalama: her sayfada 10 kayıt
    page_number = request.GET.get("page")
    item_list = paginator.get_page(page_number)

    if page_number:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    else:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(1)

    if fuel.count() == 0:
        messages.add_message(request, messages.INFO, 'İstenilen filtrede değerler bulunamadı.')

    context = {
        "fuel": item_list,
        "myFilter": myFilter
    }
    return render(request, 'report/page/general_report.html', context)

@login_required(login_url="login")
@employe_only
def car_about_report(request):
    car = Car.objects.all().order_by('-create_at')
    myFilter = CarFilter(request.GET, queryset=car)
    car = myFilter.qs

    paginator = Paginator(car, 10)
    page_number = request.GET.get("page")
    item_list = paginator.get_page(page_number)

    if page_number:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    else:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(1)

    if not car.exists():
        messages.info(request, 'İstenilen filtrede değerler bulunamadı.')

    context = {
        "car": item_list,
        "myFilter": myFilter
    }
    return render(request, 'report/page/car_about_report.html', context)

@login_required(login_url="login")
@employe_only
def lt_km_report(request):
    queryset = Fuell.objects.select_related("car", "user").all().order_by('-create_at')
    myFilter = LiterFilter(request.GET, queryset=queryset)
    filtered_data = myFilter.qs

    paginator = Paginator(filtered_data, 10)
    page_number = request.GET.get("page")
    item_list = paginator.get_page(page_number)

    item_list.adjusted_elided_pages = paginator.get_elided_page_range(page_number or 1)

    if not filtered_data.exists():
        messages.info(request, 'İstenilen filtrede değerler bulunamadı.')

    # Opsiyonel filtreyi template'e taşımak için
    filters = ""
    if request.GET.get("average"):
        try:
            filters = int(request.GET["average"])
        except ValueError:
            filters = ""

    context = {
        "fuel": item_list,
        "myFilter": myFilter,
        "filters": filters
    }
    return render(request, 'report/page/lt_km_report.html', context)

def calculate(data):
    sum_data = data.aggregate(Sum("average"))['average__sum']
    count_data = data.count()
    if count_data == 0:
        return 0
    else:
        return (sum_data/count_data)

@login_required(login_url="login")
@employe_only
def plate_report(request):
    monthly_data = []
    car_data = []
    type_data = []
    car_instance = None

    if request.method == "POST":
        plate = request.POST.get("plate", "").upper()
        try:
            car_instance = Car.objects.get(plate=plate)
            date_now = datetime.now().date()

            # İlgili aracın tüm yakıt kayıtları
            fuel_records = Fuell.objects.filter(car=car_instance)

            # Her ay için yakıt verisi hesaplama
            for month in range(1, 13):
                start_date = date(date_now.year, month, 1)
                end_day = monthrange(date_now.year, month)[1]
                end_date = date(date_now.year, month, end_day)
                monthly = calculate(fuel_records.filter(create_at__range=(start_date, end_date)))
                monthly_data.append(monthly)

            # Yıllık toplam
            yearly_range = (date(date_now.year, 1, 1), date(date_now.year + 1, 1, 1))
            car_total = calculate(fuel_records.filter(create_at__range=yearly_range))
            car_data = [car_total] * 12

            # Aynı türdeki diğer araçların toplamı
            same_type_fuel = Fuell.objects.filter(car__vehicle_type=car_instance.vehicle_type)
            type_total = calculate(same_type_fuel.filter(create_at__range=yearly_range))
            type_data = [type_total] * 12

        except Car.DoesNotExist:
            messages.info(request, f'*{plate}* plakası tanımlı değil. Lütfen geçerli bir plaka giriniz.')

    context = {
        'default': monthly_data,
        'car': car_instance,
        'default1': car_data,
        'default2': type_data
    }
    return render(request, 'report/page/plate_report.html', context)

#Export exel
def export_Liter_Excel(request):
    # Filtrelemeden gelen GET parametrelerine göre queryset'i oluştur
    queryset = Fuell.objects.select_related("car", "user").all().order_by('-create_at')
    myFilter = LiterFilter(request.GET, queryset=queryset)
    fuel_data = myFilter.qs

    # Excel response ayarları
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename=Lt_Km_Raporlama-{datetime.now().date()}.xls'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Lt_Km")

    # Başlık satırı
    columns = ["Plaka", "İlçe", "Kilometre", "Litre", "Km/Lt", "Teslim Alan", "Tarih"]
    header_style = xlwt.XFStyle()
    header_style.font.bold = True

    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, header_style)

    # Satırlar
    font_style = xlwt.XFStyle()
    date_style = xlwt.easyxf(num_format_str='DD/MM/YYYY')

    for row_num, item in enumerate(fuel_data, start=1):
        ws.write(row_num, 0, item.car.plate.upper() if item.car and item.car.plate else "", font_style)
        ws.write(row_num, 1, item.contry.upper() if item.contry else "", font_style)
        ws.write(row_num, 2, int(item.kilometer) if item.kilometer else 0, font_style)
        ws.write(row_num, 3, float(item.liter) if item.liter else 0, font_style)
        ws.write(row_num, 4, float(item.average) if item.average else 0, font_style)
        ws.write(row_num, 5, item.delivery.upper() if item.delivery else "", font_style)
        ws.write(row_num, 6, item.create_at.date() if item.create_at else "", date_style)

    wb.save(response)
    return response

def export_Excel(request):
    # Veriyi filtrele
    fuel = Fuell.objects.select_related("car", "user").all().order_by('-create_at')
    myFilter = OrderFilter(request.GET, queryset=fuel)
    fuel = myFilter.qs

    # Excel response ayarları
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename=Genel_Raporlama-{datetime.now().date()}.xls'

    # Excel kitabı ve sayfası
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Expenses")

    # Başlıklar
    columns = ["Plaka", "İlçe", "Kilometre", "Yakıt Tipi", "Litre", "Teslim alan", "Açıklama", "Tarih"]
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # Başlık satırını yaz
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, font_style)

    # Stil sıfırla
    font_style = xlwt.XFStyle()

    # Satırları yaz
    for row_num, item in enumerate(fuel, start=1):
        ws.write(row_num, 0, item.car.plate.upper() if item.car and item.car.plate else "")
        ws.write(row_num, 1, item.contry.upper() if item.contry else "")
        ws.write(row_num, 2, str(item.kilometer).upper() if item.kilometer else "")
        ws.write(row_num, 3, item.fuel_type.upper() if item.fuel_type else "")
        ws.write(row_num, 4, str(item.liter).upper() if item.liter else "")
        ws.write(row_num, 5, item.delivery.upper() if item.delivery else "")
        ws.write(row_num, 6, item.comment.upper() if item.comment else "")
        ws.write(row_num, 7, item.create_at.strftime('%Y-%m-%d %H:%M'))

    wb.save(response)
    return response


def export_Car_Excel(request):
    # Filtreleme uygulanıyor
    car_queryset = Car.objects.all().order_by('-create_at')
    myFilter = CarFilter(request.GET, queryset=car_queryset)
    cars = myFilter.qs

    # Excel ayarları
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename=Araç_Bilgileri-{datetime.now().date()}.xls'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Araç Bilgileri")

    # Başlık satırı
    columns = ["Plaka", "Marka", "Model", "Araç Cinsi", "Zimmet", "Ünvan", "Kilometre", "Yakıt Tipi", "Sahiplik", "Daire Başkanlığı", "İlçe", "Tarih", "Durum", "Açıklama"]
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, font_style)

    # Veri yazımı
    font_style = xlwt.XFStyle()
    date_style = xlwt.easyxf(num_format_str="DD/MM/YYYY")

    for row_num, row in enumerate(cars, start=1):
        ws.write(row_num, 0, row.plate or '', font_style)
        ws.write(row_num, 1, (row.brand or '').upper(), font_style)
        ws.write(row_num, 2, (row.model or '').upper(), font_style)
        ws.write(row_num, 3, row.get_vehicle_type_display() if row.vehicle_type else '', font_style)
        ws.write(row_num, 4, (row.debit or '').upper(), font_style)
        ws.write(row_num, 5, (row.title or '').upper(), font_style)
        ws.write(row_num, 6, int(row.kilometer) if row.kilometer else 0, font_style)
        ws.write(row_num, 7, row.get_fuel_type_display() if row.fuel_type else '', font_style)
        ws.write(row_num, 8, row.get_possession_display() if row.possession else '', font_style)
        ws.write(row_num, 9, row.get_department_display() if row.department else '', font_style)
        ws.write(row_num,10, row.get_contry_display() if row.contry else '', font_style)
        ws.write(row_num,11, row.create_at.date() if row.create_at else '', date_style)
        ws.write(row_num,12, row.get_status_display() if row.status else '', font_style)
        ws.write(row_num,13, row.comment or '', font_style)

    wb.save(response)
    return response
