from django.contrib import admin
from .models import Car,Fuell

# Register your models here.
class BlockNewCar(admin.ModelAdmin):
    search_fields = ("plate","brand","debit")
    list_filter = ("brand","debit","model","status","vehicle_type")
    list_display = ("plate","brand","model","debit","kilometer","vehicle_type","comment","create_at","update_at","status")

class BlockFuell(admin.ModelAdmin):
    search_fields = ("user","car")
    list_filter = ("user",)
    list_display = ("user","car","kilometer","liter","average","create_at")


admin.site.register(Car,BlockNewCar)
admin.site.register(Fuell,BlockFuell)