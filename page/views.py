from datetime import datetime,date,timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import User
from page.models import Car,Fuell,ChangeHistory
from page.decorators import *
from account.forms import CarForm,FuellForm
from django.contrib import messages
from django.db.models import ProtectedError
from django.core.paginator import Paginator
from report.filters import PlateFilter,FuelPlateFilter

@admin_only
@login_required(login_url="login")
def dataload(request):
    a = request.GET.get('data')
    table_data = []
    loaddata = []
    if a is not None:
        for item in a.splitlines():
            items = item.split(",")
            if Car.objects.filter(plate = items[0].replace(" ", "").upper()).exists():
                messages.add_message(
                        request,messages.WARNING,
                        f'"{items[0]}" Plakalı araç sisteme kayıtlı.Mevcut kayıt üzerinden işlem yapabilirsiniz.')
                return redirect("dataload")
            if len(item.split(",")) == 12:
                loaddata.append(Car(
                    plate= items[0].replace(" ", "").upper(),
                    brand= items[1].upper(),
                    model= items[2].upper(),
                    debit= items[3].upper(),
                    title= items[4].upper(),
                    kilometer= items[5],
                    vehicle_type= items[6],
                    contry= items[7],
                    department= items[8],
                    possession= items[9],
                    comment= items[11].upper()
                    ))
                table_data.append({
                    'plate': items[0].replace(" ", "").upper(),
                    'brand': items[1].upper(),
                    'model': items[2].upper(),
                    'debit': items[3].upper(),
                    'title': items[4].upper(),
                    'kilometer': items[5],
                    'vehicle_type': items[6],
                    'contry': items[7],
                    'department': items[8],
                    'possession': items[9],
                    'create_at': items[10],
                    'comment': items[11].upper()
                    })                
            elif len(item.split(",")) <= 2:
                pass
            else:
                messages.add_message(
                        request,messages.WARNING,
                        f'"{item}" Bilgiler istenilen formda değil.')
                return redirect("dataload") 
        if len(loaddata) >=1:
            Car.objects.bulk_create(loaddata)
            messages.add_message(
                            request,messages.SUCCESS,
                            f'Araç bilgileri veri tabanına eklendi.')

    return render(request ,'dataload.html',{'table_data': table_data})

@login_required(login_url="login")
def index(request):
    context = dict()
    if request.user.is_superuser:
        fuel = Fuell.objects.select_related("car","user").all()
        dateNow = datetime.now().date()
        dateTomorrow = dateNow + timedelta(days=1)
        yesterday = dateNow + timedelta(days= -1)
        yesterday = fuel.filter(create_at__range=(date(yesterday.year,yesterday.month,yesterday.day),date(dateNow.year,dateNow.month,dateNow.day)))
        month = fuel.filter(create_at__range=(date(dateNow.year,dateNow.month,1),date(dateNow.year,dateNow.month,31)))
        year = fuel.filter(create_at__range=(date(dateNow.year,1,1),date(dateNow.year,12,31)))
        a = fuel.filter(create_at__range=(date(dateNow.year,dateNow.month,dateNow.day),date(dateTomorrow.year,dateTomorrow.month,dateTomorrow.day)))
        akcakale = sum([item.liter for item in a.filter(contry="akçakale")])
        birecik = sum([item.liter for item in a.filter(contry="birecik")])
        bozova = sum([item.liter for item in a.filter(contry="bozova")])
        ceylanpınar = sum([item.liter for item in a.filter(contry="ceylanpınar")])
        halfeti = sum([item.liter for item in a.filter(contry="halfeti")])
        harran = sum([item.liter for item in a.filter(contry="harran")])
        hilvan = sum([item.liter for item in a.filter(contry="hilvan")])
        siverek = sum([item.liter for item in a.filter(contry="siverek")])
        suruç = sum([item.liter for item in a.filter(contry="suruç")])
        viranşehir = sum([item.liter for item in a.filter(contry="viranşehir")])
        merkez = sum([item.liter for item in a.filter(contry="merkez")])
        context = {
            "today": sum([item.liter for item in a]),
            "yesterday": sum([item.liter for item in yesterday]),
            "month": sum([item.liter for item in month]),
            "year": sum([item.liter for item in year]),
            "default":[merkez,akcakale,birecik,bozova,ceylanpınar,halfeti,harran,hilvan,siverek,suruç,viranşehir]
        }
        return render(request,'index.html',context)
    else:
        return redirect("refueling")

def page_not_found(request,exception):
    return render(request,"404-error.html")

def page_not_found_500(request):
    return render(request,"404-error.html")

@login_required(login_url="login")
@admin_only
def cars_home(request):
    car = Car.objects.select_related().all().order_by('-create_at')
    myFilter = PlateFilter(request.GET,queryset=car)
    car = myFilter.qs
    paginator = Paginator(car, 10)
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
        "myFilter": myFilter,
    }
    return render(request ,'page/car_home.html',context)

@login_required(login_url="login")
@admin_only
def carDelete(request,myid):
    car = Car.objects.get(id=myid)
    try:
        car.delete()
        messages.add_message(
                            request,messages.SUCCESS,
                            f'*{ car.plate }* Plakalı araç kaydı silindi.')
    except ProtectedError:
        messages.add_message(
                            request,messages.WARNING,
                            f'*{ car.plate }* Plaka diğer tablolarda kullanılmakta.Araç kaydını silmek için diğer tablolardan kayıtlı verileri silmelisiniz.!Aracı *PASİF* duruma getirebilirsiniz.' )
    return redirect('cars_home')

@login_required(login_url="login")
@admin_only
def register_new_car(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.add_message(
                        request,messages.SUCCESS,
                        f'*{ form.data["plate"] }* Kayıt başarılı.')
                return redirect ('cars_home')
            else:
                    messages.add_message(
                            request,messages.WARNING,
                            form.errors.as_ul())
        except Exception:
            messages.add_message(
                            request,messages.WARNING,
                            f'*{ form.data["plate"] }* Bu Plaka alanına sahip Araç zaten mevcut')
    else:
        form = CarForm()
    return render(request,"page/register_new_car.html",context={'form':form})

@login_required(login_url="login")
@admin_only
def carEdit(request,myid):
    car = Car.objects.get(id=myid)
    context = {
        'sel_item' :car,
        'car':Car.objects.all()
    }
    return render(request,'page/car_home.html',context)

@login_required(login_url="login")
@admin_only
def update_car(request,myid):
    car = Car.objects.get(id=myid)
    if request.method == "POST":
        form = CarForm(request.POST)
        if (form.is_valid()) or (car.plate == form.data["plate"]):
            car.brand = form.data["brand"]
            car.model = form.data["model"]
            car.debit = form.data["debit"]
            car.title = form.data["title"]
            car.kilometer = form.data["kilometer"]
            car.comment = form.data["comment"]
            car.status = form.data["status"]
            car.vehicle_type = form.data["vehicle_type"]
            car.department = form.data["department"]
            car.possession = form.data["possession"]
            car.contry = form.data["contry"]
            car.save()
            messages.add_message(
                        request,messages.SUCCESS,
                        f'*{ car.plate }* Plakalı araç bilgileri güncellendi')
            return redirect ('cars_home')
        else:
            messages.add_message(
                        request,messages.WARNING,
                        form.errors.as_text())
    else:
        form = CarForm() 
    return render(request,"account/page/register.html")

@login_required(login_url="login")
def refueling(request):
    dateNow = datetime.now().date()
    dateTomorrow = dateNow + timedelta(days=1)
    a = Fuell.objects.all().filter(contry=request.user.contry,create_at__range=(date(dateNow.year,dateNow.month,dateNow.day),date(dateTomorrow.year,dateTomorrow.month,dateTomorrow.day))).order_by('-create_at')
    litre = sum([item.liter for item in a])
    adet = a.count()
    context ={
        "liter" : litre,
        "adet" : adet,
        "fuel" : a
    }
    if request.method == "POST":
        plate = request.POST["plate"].replace(" ", "").upper()
        if plate != "":
            try:
                car = Car.objects.get(plate=plate)
                previous_amount = Fuell.objects.filter(car = car).order_by('-create_at')
                if car.status == "passive":
                    messages.add_message(
                            request,messages.INFO,
                            f'*{plate}* Plakalı araç PASİF durumda yönetici ile iletişime geçiniz.')
                else:
                    if len(previous_amount) > 0:
                        previous_amount = previous_amount[0].kilometer
                    else:
                        previous_amount = car.kilometer
                    if car.contry != request.user.contry:
                        messages.add_message(
                        request,messages.INFO,
                        f'*{plate}* Plakalı araç "{request.user.get_contry_display()}" ilçesine ait değil.')
                    
                    context = {
                        'previous_amount': previous_amount,
                        'sel_item' :car,
                        }
            except Exception:
                messages.add_message(
                request,messages.WARNING,
                f'*{plate}* Plakalı araç kayıtlarda bulunmamaktadır.')
    return render(request,"page/refueling.html",context)

@login_required(login_url="login")
def register_new_fueling(request):
    user =User.objects.get(username=request.user.username) 
    if request.method == "POST":
        data = request.POST
        car = Car.objects.get(plate = data['plate'].replace(" ", "").upper())
        previous_amount = Fuell.objects.filter(car = car).order_by('-create_at')
        if len(previous_amount) > 0:
            previous_amount = int(previous_amount[0].kilometer)
        else:
            previous_amount = int(car.kilometer)
            
        fuel = Fuell(user=user ,car =car ,kilometer = data["kilometer"],average=(int(data["kilometer"])-previous_amount)/int(data["liter"]),
                     liter = data["liter"],contry=user.contry,delivery=data['delivery']
        )
        messages.add_message(
                request,messages.SUCCESS,
                f'*{data["plate"]}* Plakalı araç için *{data["liter"]}lt.* yakıt alındı.')
        fuel.save()
        
        return redirect("refueling")
    return render(request,"page/refuling.html")

@login_required(login_url="login")
@admin_only
def fuels_home(request):
    fuel= Fuell.objects.select_related("car","user").all().order_by('-create_at')
    myFilter = FuelPlateFilter(request.GET,queryset=fuel)
    fuel = myFilter.qs
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
        "myFilter": myFilter,
    }
    return render(request ,'page/refueling_home.html',context)

@login_required(login_url="login")
@admin_only
def editfuels(request,id):
    fuell = Fuell.objects.get(id=id)
    if request.method == "POST":
        form = FuellForm(request.POST or None, instance=fuell)
        if form.is_valid():
            previous_amount = Fuell.objects.filter(car = fuell.car.id).order_by('-create_at')
            if len(previous_amount) > 0:
                previous_amount = int(previous_amount[1].kilometer)
            else:
                previous_amount = int(fuell.car.kilometer)
            fuell.average = (int(form.data["kilometer"])-previous_amount)/int(form.data["liter"])
            fuell.save()
            form.save()
            messages.add_message(
                request,messages.SUCCESS,
                f'*{fuell.car.plate}* Aracı için yakıt bilgileri güncellendi.')
            return redirect('fuels_home')
    else:
        form =FuellForm(instance=fuell)
        
    return render(request,'page/fuell_edit.html',{'form':form,'fuel':fuell})

@login_required(login_url="login")
def fuelsDelete(request,myid):
    fuel = Fuell.objects.get(id=myid)
    if request.user.is_superuser:
        fuel.delete()
    else:
        value = fuel.create_at + timedelta(hours=3)
        dateNow = datetime.now()
        dakika = int(dateNow.time().strftime('%M'))-int(value.time().strftime('%M'))
        saat =int(dateNow.time().strftime('%H'))-int(value.time().strftime('%H'))
        print(saat,dakika,fuel.create_at)
        if (saat == 0) and (dakika <= 3):
            fuel.delete()
        else:
            messages.add_message(
            request,messages.WARNING,
            "Yakıt Fişi Silme Süresi Bitmiştir.\nLütfen Yönetici İle İletişime Geçiniz.")
            return redirect('refueling')
        messages.add_message(
            request,messages.SUCCESS,
            f"*{fuel.car}* Plakalı araç için '{fuel.create_at}' tarihindeki yakıt doldurma fişi silinmiştir.")
        return redirect('refueling')
    messages.add_message(
            request,messages.SUCCESS,
            f"*{fuel.car}* Plakalı araç için '{fuel.create_at}' tarihindeki yakıt doldurma fişi silinmiştir.")
    return redirect('fuels_home')

@login_required(login_url="login")
@admin_only
def audit_log_view(request):
    logs = ChangeHistory.objects.all().order_by('-timestamp')
    
    # Sayfalama
    paginator = Paginator(logs, 10)  # Sayfada 10 kayıt göster
    page_number = request.GET.get('page')  # Sayfa numarasını al
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'page/audit_log.html', {'page_obj': page_obj})