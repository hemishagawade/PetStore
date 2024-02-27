from django.contrib import admin
from PetApp.models import Pet, Cart, Orders

# Register your models here.
class PetAdmin(admin.ModelAdmin):
    list_display = ['id','name','type','breed','gender','age','description','price','p_image']
    list_filter = ['type','breed','price']

admin.site.register(Pet, PetAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','uid','pid','quantity']
    list_filter = ['uid']

admin.site.register(Cart, CartAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id','orderid','uid','pid','quantity']

admin.site.register(Orders, OrdersAdmin)
