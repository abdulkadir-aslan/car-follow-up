from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404, handler500
from page.views import *


urlpatterns = [
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('notifications/', notifications_view, name='notifications'),
    path('car/<int:car_id>/zimmet-fisi-ekle/', zimmet_fisi_ekle, name='zimmet_fisi_ekle'),
    path('zimmet-fisi/<int:zimmet_fisi_id>/sil/', zimmet_fisi_sil, name='zimmet_fisi_sil'),

    
    path('', index,name='home'),
    #audit log
    path("log_delete/<int:log_id>/",log_delete,name="log_delete"),
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
handler500 = "page.views.server_error"