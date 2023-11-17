from django.contrib import admin
from django.core.management import call_command

from storage.models import Client, Box, Storage, Order


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_email', 'address',
                    'phonenumber']
    readonly_fields = ['user']
    inlines = [
        OrderInline
    ]
    change_list_template = "admin/client.html"

class BoxInline(admin.TabularInline):
    model = Box
    extra = 0

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ['numer', 'address', 'feature']
    inlines = [
        BoxInline
    ]

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['name', 'storage', 'length', 'width', 'height',
                    'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'storage', 'box', 'client', 'price']
    change_list_template = "admin/order.html"
