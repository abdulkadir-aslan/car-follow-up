from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from page.views import *


urlpatterns = [
    path('', index,name='home'),
    #audit log
    path('audit_log/',audit_log_view,name="audit_log"),
    #Dataload
    path('dataload/',dataload,name="dataload"),
    #Reports
    path('report/',include('report.urls')),
    #account
    path('',include('account.urls')),
    path('admin/', admin.site.urls),
    #Car
    path("cars_home",cars_home,name="cars_home"),
    path("car_delete/<int:myid>/",carDelete,name="car_delete"),
    path("register_new_car",register_new_car,name="register_new_car"),
    path("car_edit/<int:myid>/",carEdit,name="car_edit"),
    path("update_car/<int:myid>/",update_car,name="update_car"),
    #Fuel
    path("edit_fuell/<int:id>",editfuels,name="editfuels"),
    path("fuels_home",fuels_home,name="fuels_home"),
    path("refueling",refueling,name="refueling"),
    path("register_new_fueling",register_new_fueling,name="register_new_fueling"),
    path("fuels_delete/<int:myid>/",fuelsDelete,name="fuels_delete"),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)

handler404 = "page.views.page_not_found"
handler500 = "page.views.page_not_found_500"