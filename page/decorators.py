from django.http import HttpResponse
from django.shortcuts import redirect


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bu sayfaya Erişim izniniz bulunmamaktadır.')
    
    return wrapper_function

def employe_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if (request.user.is_admin) or (request.user.is_employee) or (request.user.is_maneger):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bu sayfaya Erişim izniniz bulunmamaktadır.')
    
    return wrapper_function

def maneger_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if (request.user.is_admin) or (request.user.is_maneger):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bu sayfaya Erişim izniniz bulunmamaktadır.')
    
    return wrapper_function

def mechanical_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if (request.user.is_admin) or (request.user.is_mechanical):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bu sayfaya Erişim izniniz bulunmamaktadır.')
    
    return wrapper_function