from django.contrib import admin
from django.contrib.auth.models import User
from django.core.management import call_command

from storage.models import Box, Client, LinkStatistics, Order, Storage

User._meta.get_field('email')._unique = True


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_email', 'address',
                    'phonenumber', 'need_call', 'need_invoice']
    readonly_fields = ['user']
    inlines = [
        OrderInline
    ]
    list_filter = ["need_call", "need_invoice"]
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
    list_display = ['pk', 'storage', 'box', 'client', 'days_left', 'send_message', 'paid']
    list_filter = ['paid', 'send_message']
    change_list_template = "admin/order.html"


@admin.register(LinkStatistics)
class LinkStatisticsAdmin(admin.ModelAdmin):
    readonly_fields = ('transitions',
                       'bitlink')
    list_display = ('bitlink',
                    'transitions')
