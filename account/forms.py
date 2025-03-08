from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from page.models import Car, Fuell

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
    class Meta:
        model = Fuell
        fields = [
            'kilometer',
            'liter',
            'delivery',
        ]