from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from page.models import Car, Fuell,ZimmetFisi
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email',
                  'password1','password2','status','contry'
        )
        widgets ={
            'username' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'kullanıcı adı'},),
            'first_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'adı'},),
            'last_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'soyadı'},),
            'status' : forms.Select(attrs={'class': 'form-select'},),
            'contry' : forms.Select(attrs={'class': 'form-select'},),
        }
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'name@example.com'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}

class SignUpEditForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
   
    class Meta:
        model = User
        fields = ('username','first_name','last_name',
                  'email','status','contry'
        )
        
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('plate','brand','model',
                  'debit','title','kilometer',
                  'comment','status','vehicle_type',
                  'possession','department','fuel_type','contry'
        )
        widgets ={
            'plate' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plakayı giriniz'},),
            'brand' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Araç markasını giriniz'},),
            'model' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Araç modelini giriniz'},),
            'debit' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adı-soyadı(zimmetlinin)'},),
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zimmetin ünvanı'},),
            'kilometer' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Araç Teslim Alınma Km"sini giriniz'},),
            'comment' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açıklma'},),
            'status' :  forms.Select(attrs={'class': 'form-select'},),
            'vehicle_type' : forms.Select(attrs={'class': 'form-select'},),
            'possession' : forms.Select(attrs={'class': 'form-select'},),
            'department' : forms.Select(attrs={'class': 'form-select'},),
            'fuel_type' :forms.Select(attrs={'class': 'form-select'},),
            'contry' :forms.Select(attrs={'class': 'form-select'},),
        }

class UpdateUserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    class Meta:
        model = User
        fields = ('password1','password2')
    
class FuellForm(forms.ModelForm):
    plate = forms.CharField(label="Plaka", max_length=20)

    class Meta:
        model = Fuell
        fields = [
            'kilometer',
            'liter',
            'delivery',
            'comment',
        ]

    def __init__(self, *args, **kwargs):
        super(FuellForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.car:
            self.fields['plate'].initial = self.instance.car.plate

    def clean_plate(self):
        # Girilen değeri al, boşlukları sil, büyük harfe çevir
        new_plate = self.cleaned_data.get('plate').replace(" ", "").upper()
        current_car = self.instance.car

        try:
            # Silinmiş boşluklarla karşılaştırma yap
            Car.objects.get(plate=new_plate)
        except Car.DoesNotExist:
            raise ValidationError("Bu plaka sistemde kayıtlı değil. Lütfen mevcut bir araç seçin.")

        return new_plate

    def save(self, commit=True):
        instance = super(FuellForm, self).save(commit=False)
        new_plate = self.cleaned_data.get('plate').replace(" ", "").upper()

        # Eğer plaka farklıysa, güncelle
        if new_plate and instance.car.plate != new_plate:
            car = Car.objects.get(plate=new_plate)
            instance.car = car

        if commit:
            instance.save()
        return instance

class ZimmetFisiForm(forms.ModelForm):
    class Meta:
        model = ZimmetFisi
        fields = ['car', 'file']
    
    car = forms.ModelChoiceField(queryset=Car.objects.all(), required=True)
    file = forms.FileField(required=True)
    widgets ={
            'plate' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plakayı giriniz'},),
    }
    