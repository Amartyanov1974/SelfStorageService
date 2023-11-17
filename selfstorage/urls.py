"""selfstorage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from storage import actions, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('faq', views.faq, name='faq'),
    path('boxes', views.boxes, name='boxes'),
    path('my_rent', views.my_rent, name='my_rent'),
    path('deauth', views.deauth, name='deauth'),
    path('generate_qr_code/', views.generate_qr_code, name='generate_qr_code'),
    path('create_client', actions.create_client, name='create_client'),
    path('send_check', actions.send_check, name='send_check'),
    path('send_message', actions.send_message, name='send_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
