from django.contrib import admin
from .models import Car,Fuell,ChangeHistory,ZimmetFisi,Notification

class ZimmetFisiAdmin(admin.ModelAdmin):
    list_display = ('car', 'file', 'created_at', 'uploaded_by')
    search_fields = ('car__plate', 'created_at',)
    list_filter = ('created_at',)

admin.site.register(ZimmetFisi, ZimmetFisiAdmin)

class ChangeHistoryAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'object_id', 'field_name', 'old_value', 'new_value', 'change_type', 'user', 'timestamp')
    list_filter = ('model_name', 'change_type', 'timestamp')

admin.site.register(ChangeHistory, ChangeHistoryAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','message','is_read','created_at')
    list_filter = ('user','message','is_read','created_at')

admin.site.register(Notification, NotificationAdmin)
# Register your models here.
class BlockNewCar(admin.ModelAdmin):
    search_fields = ("plate","brand","debit")
    list_filter = ("brand","debit","model","status","vehicle_type")
    list_display = ("plate","brand","model","debit","kilometer","vehicle_type","comment","create_at","update_at","status")

class BlockFuell(admin.ModelAdmin):
    search_fields = ("user","car")
    list_filter = ("user",)
    list_display = ("user","car","kilometer","liter","fuel_type","average","create_at")


admin.site.register(Car,BlockNewCar)
admin.site.register(Fuell,BlockFuell)