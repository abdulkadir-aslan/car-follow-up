from django.shortcuts import render ,redirect
from .forms import SignUpForm,LoginForm,SignUpEditForm,UpdateUserForm
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth import get_user_model
from account.models import User
from django.contrib.auth.decorators import login_required
from page.decorators import *
from django.contrib import messages
from django.db.models import ProtectedError


def login_request(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password = password)
            if user is not None:
                login(request,user)
                if request.user.status == 'active':
                    messages.add_message(
                        request,messages.SUCCESS,
                        'Giriş Başarılı.' )
                    return redirect('home')
                else:
                    logout(request)
                    messages.add_message(
                        request,messages.INFO,
                        "Kullanıcı 'Pasif' durumda yönetici ile iletişime geçiniz." )
            else:
                messages.add_message(
                request,messages.WARNING,
                        "Kullanıcı Adı yada Parola yanlış" )
        else:
            messages.add_message(
                request,messages.WARNING,
                        "Lütfen ilgili alanları doldurunuz." )
    return render(request,"account/page/login.html")
    
def logout_request(request):
    messages.add_message(
                request,messages.WARNING,
                        f"*{request.user.username}* Kullanıcısı için oturum kapatıldı." )
    logout(request)
    return redirect("login")


@login_required(login_url="login")
@admin_only
def register_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.add_message(
                request,messages.SUCCESS,
                        f"*{user.username}* Kullanıcısı kaydedildi." )
            return redirect ('users_home')
        else:
            messages.add_message(
            request,messages.WARNING,
            form.errors.as_ul())
    else:
        form = SignUpForm()
    return render(request,"account/page/register.html",context={'form':form})

@login_required(login_url="login")
@admin_only
def users_home(request):
    context = dict()
    context["users"]= get_user_model().objects.all()
    return render(request ,'account/page/login_home.html',context)

@login_required(login_url="login")
@admin_only
def userDelete(request,myid):
    user = User.objects.get(id=myid)
    if user.is_superuser:
        messages.add_message(
        request,messages.WARNING,
        f'*{user.username}* kullanıcısı Yönetici olduğundan silinemez.')
    else:
        try:
            user.delete()
            messages.add_message(
            request,messages.SUCCESS,
            f'*{user.username}* kullanıcısı silindi.')
        except ProtectedError:
             messages.add_message(
                            request,messages.WARNING,
                            f'*{ user.username }* Kullanıcı diğer tablolarda kullanılmakta.Kullanıcı kaydını silmek için diğer tablolardan kayıtlı verileri silmelisiniz.!Kullanıcıyı *PASİF* duruma getirebilirsiniz.' )
    return redirect('users_home')

@login_required(login_url="login")
@admin_only
def userEdit(request,myid):
    user = User.objects.get(id=myid)
    context = {
        'sel_item' :user,
        'users':get_user_model().objects.all()
    }
    return render(request,'account/page/login_home.html',context)

@login_required(login_url="login")
@admin_only
def updateUser(request,myid):
    user = User.objects.get(id=myid)
    if request.method == "POST":
        form = SignUpEditForm(request.POST)
        if (form.is_valid()) or (user.username == form.data["username"]):
            if (user.is_superuser) and (form.data["status"]=="passive"):
                messages.add_message(
                        request,messages.WARNING,
                        f'*{user.username}* kullanıcısı Yönetici olduğundan PASİF duruma getirilemez.')
                return redirect ('users_home')
            else:
                user.username = form.data["username"]
                user.email = form.data["email"]
                user.first_name = form.data["first_name"]
                user.last_name = form.data["last_name"]
                user.status = form.data["status"]
                user.contry = form.data["contry"]
                user.save()
                messages.add_message(
                request,messages.SUCCESS,
                f'*{user.username}* kullanıcısına ait bilgiler güncellendi.')
                return redirect ('users_home')
    else:
        form = SignUpEditForm() 
    return render(request,"account/page/register.html")
        
def update_password(request,myid):
    user = User.objects.get(username=myid)
    if request.method == "POST":
        form = UpdateUserForm(request.POST)
        print(form.data)
        if form.is_valid():
            user.set_password(form.data["password1"])
            user.save()
            messages.add_message(
                request,messages.SUCCESS,
                f'*{user.username}* Kullanıcısı için şifre güncellendi.')
            return redirect('users_home')            
        else:
            messages.add_message(
                request,messages.WARNING,
                form.errors.as_text())
    return render(request,"account/page/update_password.html")