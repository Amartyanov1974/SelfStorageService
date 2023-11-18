from django.urls import path

from storage.views import storages, box_select, create_order

app_name = 'storages'

urlpatterns = [
    path('', storages, name='index'),
    path('box_select/<int:storage_id>', box_select, name='box_select'),
    path('order_confirmation/<int:box_id>', create_order, name='order_confirmation'),

]
