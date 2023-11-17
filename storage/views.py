import qrcode
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from storage.actions import (
    auth, deauth, registration, send_message, sendpasswd, update_client)
from storage.models import Client

User._meta.get_field('email')._unique = True

def index(request):
    context = {}
    if 'message' in request.session and request.session['message']:
        context = {
        'message': request.session.get('message'),
        }
        request.session['message'] =''

    elif 'EMAIL_CREATE' in request.POST:
        registration(request)
        return redirect('/')

    elif 'EMAIL' in request.POST:
        auth(request)
        return redirect('/')

    elif 'EMAIL_FORGET' in request.POST:
        sendpasswd(request)
        return redirect('/')

    elif 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            }

    return render(request, 'index.html', context=context)


def faq(request):
    context = {}
    if 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            }
    return render(request, 'faq.html', context=context)


def boxes(request):
    context = {}
    if 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            }
    return render(request, 'boxes.html', context=context)


def generate_qr_code(request):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
# данные где забрать заказ
    client_data = Client.objects.get(user=request.user)
    qr.add_data(client_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response




def my_rent(request):
    context = {}
    if 'PHONE_EDIT' in request.POST:
        update_client(request)
    if 'user_name' in request.session:
        client = Client.objects.get(user=request.user)
        context = {
            'username': request.session['user_name'],
            'client': client,
            }
    return render(request, 'my-rent.html', context=context)
