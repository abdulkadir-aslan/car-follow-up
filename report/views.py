from django.shortcuts import render
from page.models import Car,Fuell
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from page.decorators import *
from datetime import datetime,date
from django.db.models import Sum
from django.core.paginator import Paginator
from .filters import OrderFilter,CarFilter,LiterFilter

import xlwt
from django.http import HttpResponse


@login_required(login_url="login")
@employe_only
def general_report(request):
    fuel = Fuell.objects.select_related("car","user").all().order_by('-create_at')
    myFilter = OrderFilter(request.GET,queryset=fuel)
    fuel = myFilter.qs
    global fuel_general_report
    fuel_general_report = fuel
    paginator = Paginator(fuel, 10) # Show 10 contacts per page.
    page_number = request.GET.get("page")
    item_list = paginator.get_page(page_number)
    if page_number is not None:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    else:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(1)
    if fuel.count() ==0:
        messages.add_message(
                        request,messages.INFO,
                        'İstenilen filtrede değerler bulunamadı.')
        fuel = []
    context ={
        "fuel":item_list,
        "myFilter": myFilter
    }
    return render(request,'report/page/general_report.html',context)

@login_required(login_url="login")
@employe_only
def car_about_report(request):
    car = Car.objects.select_related().all().order_by('-create_at')
    myFilter = CarFilter(request.GET,queryset=car)
    car = myFilter.qs
    global car_about_report
    car_about_report = car
    paginator = Paginator(car, 10) # Show 10 contacts per page.
    page_number = request.GET.get("page")
    item_list = paginator.get_page(page_number)
    if page_number is not None:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    else:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(1)
    if car.count() ==0:
        messages.add_message(
                        request,messages.INFO,
                        'İstenilen filtrede değerler bulunamadı.')
        car = []
    context ={
        "car":item_list,
        "myFilter": myFilter
    }
    return render(request,'report/page/car_about_report.html',context)

@login_required(login_url="login")
@employe_only
def lt_km_report(request):
    car = Fuell.objects.select_related("car","user").all().order_by('-create_at')
    myFilter = LiterFilter(request.GET,queryset=car)
    car = myFilter.qs
    global liter_report
    liter_report = car
    paginator = Paginator(car, 10) # Show 10 contacts per page.
    page_number = request.GET.get("page")
    item_list = paginator.get_page(page_number)
    if page_number is not None:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    else:
        item_list.adjusted_elided_pages = paginator.get_elided_page_range(1)
    if car.count() ==0:
        messages.add_message(
                        request,messages.INFO,
                        'İstenilen filtrede değerler bulunamadı.')
        car = []
    filters = ""
    if request.GET.get("average") is not None:
        if (request.GET["average"] != ""):
            filters = int(request.GET.get("average"))
    context ={
        "fuel":item_list,
        "myFilter": myFilter,
        "filters":filters
    }
    return render(request,'report/page/lt_km_report.html',context)

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
    default = []
    default1 = []
    default2 = []
    cars = ''
    if request.method == "POST":
        try:
            dateNow = datetime.now().date()
            car = Car.objects.get(plate =request.POST["plate"].upper())
            fuel = Fuell.objects.all().filter(car =car)
            Jan = calculate(fuel.filter(create_at__range=(date(dateNow.year,1,1),date(dateNow.year,2,1))))
            Feb = calculate(fuel.filter(create_at__range=(date(dateNow.year,2,1),date(dateNow.year,3,1))))
            Mar = calculate(fuel.filter(create_at__range=(date(dateNow.year,3,1),date(dateNow.year,4,1))))
            Apr = calculate(fuel.filter(create_at__range=(date(dateNow.year,4,1),date(dateNow.year,5,1))))
            May = calculate(fuel.filter(create_at__range=(date(dateNow.year,5,1),date(dateNow.year,6,1))))
            Jun = calculate(fuel.filter(create_at__range=(date(dateNow.year,6,1),date(dateNow.year,7,1))))
            Jul = calculate(fuel.filter(create_at__range=(date(dateNow.year,7,1),date(dateNow.year,8,1))))
            Aug = calculate(fuel.filter(create_at__range=(date(dateNow.year,8,1),date(dateNow.year,9,1))))
            Sep = calculate(fuel.filter(create_at__range=(date(dateNow.year,9,1),date(dateNow.year,10,1))))
            Oct = calculate(fuel.filter(create_at__range=(date(dateNow.year,10,1),date(dateNow.year,11,1))))
            Nov = calculate(fuel.filter(create_at__range=(date(dateNow.year,11,1),date(dateNow.year,12,1))))
            Dec = calculate(fuel.filter(create_at__range=(date(dateNow.year,12,1),date(dateNow.year+1,1,1))))
            default = [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,Oct]
            cars = car
            df1 = calculate(fuel.filter(create_at__range=(date(dateNow.year,1,1),date(dateNow.year+1,1,1))))
            fuel = Fuell.objects.all().filter(car__vehicle_type =car.vehicle_type)
            df2 = calculate(fuel.filter(create_at__range=(date(dateNow.year,1,1),date(dateNow.year+1,1,1))))
            default1 = [df1,df1,df1,df1,df1,df1,df1,df1,df1,df1,df1,df1]
            default2 = [df2,df2,df2,df2,df2,df2,df2,df2,df2,df2,df2,df2]
        except :
            messages.add_message(
            request,messages.INFO,
            f'*{request.POST["plate"].upper()}* Plakası tanımlı değil.Lütfen geçerli bir plaka giriniz..')
    context = {
        'default':default,
        'car':cars,
        'default1':default1,
        'default2':default2
    }
    print(context)
    return render(request,'report/page/plate_report.html',context)

#Export exel
def export_Liter_Excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Lt/Km Raporlama-'+\
        str(datetime.now().date())+'.xls'
    wb = xlwt.Workbook(encoding = "utf-8")
    ws = wb.add_sheet("Expenses")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    column = ["Plaka","İlçe","Kilometre","Litre","Km/Lt","Teslim alan","Tarih"]

    for col_num in range(len(column)):
        ws.write(row_num,col_num,column[col_num],font_style)

    font_style = xlwt.XFStyle()

    rows = liter_report.values_list("car__plate","contry","kilometer","liter","average","delivery","create_at")

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]).upper(),font_style)
    wb.save(response)

    return response

def export_Excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Genel_Raporlama-'+\
        str(datetime.now().date())+'.xls'
    wb = xlwt.Workbook(encoding = "utf-8")
    ws = wb.add_sheet("Expenses")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    column = ["Plaka","İlçe","Kilometre","Yakıt Tipi","Litre","Teslim alan","Açıklama","Tarih"]

    for col_num in range(len(column)):
        ws.write(row_num,col_num,column[col_num],font_style)

    font_style = xlwt.XFStyle()

    rows = fuel_general_report.values_list("car__plate","contry","kilometer","fuel_type","liter","delivery","comment","create_at")

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]).upper(),font_style)
    wb.save(response)

    return response

def export_Car_Excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Araç Bilgileri-'+\
        str(datetime.now().date())+'.xls'
    wb = xlwt.Workbook(encoding = "utf-8")
    ws = wb.add_sheet("Expenses")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    column = ["Plaka","Marka","Model","Araç Cinsi","Zimmet","Ünvan","Kilometre","Yakt Tipi","Sahiplik","Daire Başkanlığı","iLÇE","Tarih","Durum","Açıklama"]

    for col_num in range(len(column)):
        ws.write(row_num,col_num,column[col_num],font_style)

    font_style = xlwt.XFStyle()
    date_style =xlwt.easyxf(num_format_str="dd/mm/yyyy") 
    rows = car_about_report
    for row in rows:
        row_num += 1
        ws.write(row_num,0,row.plate,font_style)
        ws.write(row_num,1,row.brand.upper(),font_style)
        ws.write(row_num,2,row.model.upper(),font_style)
        ws.write(row_num,3,row.get_vehicle_type_display(),font_style)
        ws.write(row_num,4,row.debit.upper(),font_style)
        ws.write(row_num,5,row.title.upper(),font_style)
        ws.write(row_num,6,int(row.kilometer),font_style)
        ws.write(row_num,7,row.get_fuel_type_display(),font_style)
        ws.write(row_num,8,row.get_possession_display(),font_style)
        ws.write(row_num,9,row.get_department_display(),font_style)
        ws.write(row_num,10,row.get_contry_display(),font_style)
        ws.write(row_num,11,datetime.date(row.create_at),date_style)
        ws.write(row_num,12,row.get_status_display(),font_style)
        ws.write(row_num,13,row.comment,font_style)
    wb.save(response)

    return response
