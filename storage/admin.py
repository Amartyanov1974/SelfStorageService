from django.contrib import admin

from storage.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_email', 'address',
                    'phonenumber']
    readonly_fields = ['user']
