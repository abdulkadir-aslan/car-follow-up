from datetime import datetime,date,timedelta
from calendar import monthrange
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import User
from page.models import Car,Fuell,ChangeHistory,ZimmetFisi,Notification
from page.decorators import *
from account.forms import CarForm,FuellForm,ZimmetFisiForm
from django.contrib import messages
from django.db.models import ProtectedError
from django.core.paginator import Paginator
from report.filters import PlateFilter,FuelPlateFilter,ChangeHistoryFilter
from urllib.parse import urlencode
import os
from django.utils.timezone import now

@login_required(login_url="login")
def notifications_view(request):
    notification_type = request.GET.get('type', 'active')  # 'active' veya 'read'

    if notification_type == 'read':
        notifications = request.user.notifications.filter(is_read=True).order_by('-created_at')
    else:
        notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')

    # Paginator ekliyoruz
    paginator = Paginator(notifications, 10)  # Sayfa başına 10 bildirim
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        ids = request.POST.getlist('read_ids')
        if notification_type == 'active':
            # Aktif bildirimleri okundu olarak işaretle
            Notification.objects.filter(id__in=ids, user=request.user).update(is_read=True)
        else:
            # Okundu bildirimleri tekrar aktif (okunmamış) yap
            Notification.objects.filter(id__in=ids, user=request.user).update(is_read=False)

        # POST sonrası aynı sekmeye yönlendirelim
        return redirect(f"{request.path}?type={notification_type}")

    return render(request, "page/notifications.html", {
        "notifications": page_obj,  # Burada doğrudan `page_obj`'yi gönderiyoruz
        "notification_type": notification_type,
    })

@login_required(login_url="login")
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    return redirect('notifications')

@login_required(login_url="login")
def zimmet_fisi_ekle(request, car_id):
    car = Car.objects.get(id=car_id)
    zimmet_fisleri = ZimmetFisi.objects.filter(car=car).order_by('-created_at')
    if request.method == 'POST':
        form = ZimmetFisiForm(request.POST, request.FILES)
        if form.is_valid():
            zimmet_fisi = form.save(commit=False)
            zimmet_fisi.uploaded_by = request.user
            zimmet_fisi.save()
            messages.success(request, 'Zimmet fişi başarıyla eklendi.')
            return redirect('zimmet_fisi_ekle', car_id=car.id)
    else:
        form = ZimmetFisiForm(initial={'car': car})

    return render(request, 'page/zimmet_fisi_ekle.html', {'form': form, 'car': car,'zimmet_fisleri': zimmet_fisleri,})

@login_required(login_url="login")
def zimmet_fisi_sil(request, zimmet_fisi_id):
    zimmet_fisi = ZimmetFisi.objects.get(id=zimmet_fisi_id)
    car = zimmet_fisi.car
    # PDF dosyasını sil
    if zimmet_fisi.file:
        pdf_path = zimmet_fisi.file.path  # Dosya yolu
        if os.path.exists(pdf_path):
            os.remove(pdf_path)  # Dosyayı sil
    zimmet_fisi.delete()
    messages.success(request, 'Zimmet fişi başarıyla silindi.')
    return redirect('zimmet_fisi_ekle', car_id=car.id)

@admin_only
@login_required(login_url="login")
def dataload(request):
    raw_data = request.GET.get('data', '')
    table_data = []
    to_create = []

    if raw_data:
        lines = raw_data.strip().splitlines()

        for line in lines:
            items = [i.strip() for i in line.split(",")]

            # Geçersiz satır
            if len(items) != 12:
                if len(items) <= 2:
                    continue  # Boş veya başlık satırı gibi görünüyor
                messages.warning(request, f'"{line}" satırı istenilen formda değil.')
                return redirect("dataload")

            plate = items[0].replace(" ", "").upper()

            # Araç zaten kayıtlıysa
            if Car.objects.filter(plate=plate).exists():
                messages.warning(request, f'"{plate}" plakalı araç sistemde mevcut.')
                return redirect("dataload")

            # Hazırlanan veri kaydedilecek ve görüntülenecek listeye ekleniyor
            car_data = {
                'plate': plate,
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
                'comment': items[11].upper(),
            }

            to_create.append(Car(**{k: v for k, v in car_data.items() if k != 'create_at'}))
            table_data.append(car_data)

        # Veritabanına ekleme
        if to_create:
            Car.objects.bulk_create(to_create)
            messages.success(request, f'{len(to_create)} araç başarıyla eklendi.')

    return render(request, 'dataload.html', {'table_data': table_data})

@login_required(login_url="login")
def index(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("refueling")

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    start_of_month = date(today.year, today.month, 1)
    end_of_month = date(today.year, today.month, monthrange(today.year, today.month)[1])
    start_of_year = date(today.year, 1, 1)
    end_of_year = date(today.year, 12, 31)
    yesterday = today - timedelta(days=1)

    # Yakıt verilerini çek
    fuel = Fuell.objects.select_related("car", "user").all()

    # Tarih aralığına göre filtreler
    today_fuel = fuel.filter(create_at__range=(today, tomorrow))
    yesterday_fuel = fuel.filter(create_at__range=(yesterday, today))
    month_fuel = fuel.filter(create_at__range=(start_of_month, end_of_month))
    year_fuel = fuel.filter(create_at__range=(start_of_year, end_of_year))

    # İlçe bazlı toplamlar
    districts = ["merkez", "akçakale", "birecik", "bozova", "ceylanpınar", "halfeti",
                 "harran", "hilvan", "siverek", "suruç", "viranşehir"]

    district_liters = [
        sum(item.liter for item in today_fuel.filter(contry=ilce)) for ilce in districts
    ]

    context = {
        "today": sum(item.liter for item in today_fuel),
        "yesterday": sum(item.liter for item in yesterday_fuel),
        "month": sum(item.liter for item in month_fuel),
        "year": sum(item.liter for item in year_fuel),
        "default": district_liters
    }

    return render(request, 'index.html', context)

def page_not_found(request,exception):
    return render(request,"404-error.html",status=404)

def server_error(request):
    return render(request,"404-error.html",500)

@login_required(login_url="login")
@employe_only
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
@employe_only
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
@employe_only
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
@employe_only
def update_car(request,myid):
    car = Car.objects.get(id=myid)
    if request.method == "POST":
        form = CarForm(request.POST or None, instance=car)
        if (form.is_valid()):
            form.save()
            messages.add_message(
                        request,messages.SUCCESS,
                        f'*{ car.plate }* Plakalı araç bilgileri güncellendi')
            return redirect ('cars_home')
        else:
            messages.add_message(
                        request,messages.WARNING,
                        form.errors.as_text())
    else:
        form = CarForm(instance=car) 
    context = {
        'form' :form,
    }
    return render(request,'page/car_home.html',context)

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
        # Aynı araç, aynı kilometre ve aynı gün kontrolü
        today = now().date()
        if Fuell.objects.filter(user=user,car=car, kilometer=data['kilometer'], create_at__date=today).exists():
            messages.warning(request, f"{car.plate} aracı için bu kilometrede ({data['kilometer']}) zaten bugün bir kayıt var.")
            return redirect("refueling")
        fuel = Fuell(user=user ,car =car ,fuel_type=data["fuel_type"],kilometer = data["kilometer"],average=(int(data["kilometer"])-previous_amount)/int(data["liter"]),
                     liter = data["liter"],contry=user.contry,delivery=data['delivery'],comment=data['comment']
        )
        messages.add_message(
                request,messages.SUCCESS,
                f'*{data["plate"]}* Plakalı araç için *{data["liter"]}lt.* yakıt alındı.')
        fuel.save()
        
        return redirect("refueling")
    return render(request,"page/refuling.html")

@login_required(login_url="login")
@employe_only
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
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = urlencode(query_params)
    context ={
        "fuel":item_list,
        "myFilter": myFilter,
        "query_string": query_string,
    }
    return render(request ,'page/refueling_home.html',context)

@login_required(login_url="login")
@employe_only
def editfuels(request, id):
    fuell = get_object_or_404(Fuell, id=id)

    # Önceki yakıt kaydının kilometresi
    previous_fuels = Fuell.objects.filter(car=fuell.car).exclude(id=fuell.id).order_by('-create_at')
    if previous_fuels.exists():
        previous_amount = previous_fuels[0].kilometer
    else:
        previous_amount = fuell.car.kilometer  # araç km'si baz alınır

    if request.method == "POST":
        form = FuellForm(request.POST, instance=fuell)
        if form.is_valid():
            km = int(form.cleaned_data["kilometer"])
            liter = float(form.cleaned_data["liter"])
            previous_amount = int(previous_amount)
            # Ortalama hesaplama
            if liter > 0:
                fuell.average = (km - previous_amount) / liter
            else:
                fuell.average = 0  # litre 0 ise hata önlemek için 0 yapabiliriz

            fuell = form.save(commit=False)
            fuell.average = fuell.average
            fuell.save()

            messages.success(request, f'*{fuell.car.plate}* Aracı için yakıt bilgileri güncellendi.')
            return redirect('fuels_home')
        else:
            # Form hatalarını mesaj olarak göster
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f"Plaka: {error}")
    else:
        form = FuellForm(instance=fuell)

    return render(request, 'page/fuell_edit.html', {'form': form, 'fuel': fuell, 'previous_amount': previous_amount})

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
    # Formu oluşturuyoruz
    filter = ChangeHistoryFilter(request.GET, queryset=ChangeHistory.objects.all().order_by('-timestamp'))

    # Sayfalama işlemi
    paginator = Paginator(filter.qs, 10)  # Filter'lanan queryset'e göre sayfalama
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'page/audit_log.html', {'page_obj': page_obj, 'filter': filter})

def log_delete(request, log_id):
    log = get_object_or_404(ChangeHistory, id=log_id)
    log.delete()
    messages.add_message(
    request,messages.SUCCESS,
            f" Log kaydı silinmiştir.")
    return redirect('audit_log')