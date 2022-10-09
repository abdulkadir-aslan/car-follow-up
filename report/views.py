from fileinput import filename
from django.shortcuts import render
from django.views.generic import View
from page.models import Car,Fuell
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from page.decorators import *
from datetime import datetime,date,timedelta
from django.db.models import Sum
from django.core.paginator import Paginator
from .filters import OrderFilter

import xlwt
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

@login_required(login_url="login")
@admin_only
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
@admin_only
def car_about_report(request):
    car = Car.objects.all().filter(status="active")
    if request.method == "POST":
        if (request.POST["vehicle_type"] != ""):
            car = car.filter(vehicle_type=request.POST["vehicle_type"])
        if (request.POST["possession"] != ""):
            car = car.filter(possession=request.POST["possession"])
        if (request.POST["contry"] != ""):
            car = car.filter(contry=request.POST["contry"])
        if (request.POST["department"] != ""):
            car = car.filter(department=request.POST["department"])
    
    if car.count() ==0:
        messages.add_message(
                        request,messages.INFO,
                        'İstenilen filtrede değerler bulunamadı.')
        car = []
    context = { 
            "car":car,
               }
    return render(request,'report/page/car_about_report.html',context)

@login_required(login_url="login")
@admin_only
def lt_km_report(request):
    filters = ""
    fuel = Fuell.objects.select_related("car","user").all()
    if request.method == "POST":
        if request.POST["possession"] != "":
            fuel = fuel.filter(car__possession=request.POST["possession"])
       
        if (request.POST["contry"] != ""):
            fuel = fuel.filter(contry=request.POST["contry"])
            
        if request.POST["vehicle_type"] != "":
            fuel = fuel.filter(car__vehicle_type=request.POST["vehicle_type"])
        
        if (request.POST["average"] != ""):
            filters = int(request.POST["average"])
    
    if fuel.count() ==0:
        messages.add_message(
        request,messages.INFO,
        'İstenilen filtrede değerler bulunamadı.')
        fuel = []
    context = { 
        "fuel":fuel,
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
@admin_only
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
    return render(request,'report/page/plate_report.html',context)

def export_Excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Genel_Raporlama-'+\
        str(datetime.now().date())+'.xls'
    wb = xlwt.Workbook(encoding = "utf-8")
    ws = wb.add_sheet("Expenses")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    column = ["Plaka","İlçe","Kilometre","Litre","Teslim alan","Tarih"]
    
    for col_num in range(len(column)):
        ws.write(row_num,col_num,column[col_num],font_style)
    
    font_style = xlwt.XFStyle()
    
    rows = fuel_general_report.values_list("car__plate","contry","kilometer","liter","delivery","create_at")
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    
    return response
            


   
def pdf_report_create(request):
    # products = Fuell.objects.all().filter(contry="birecik",car__vehicle_type="mount")
    
    template_path = 'expenses/pdf-output.html'

    context = {'fuel': fuel_general_report}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="products_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response