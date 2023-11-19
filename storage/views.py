import datetime
import random
from urllib.parse import unquote

import qrcode
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from storage.actions import (auth, create_empty_order, deauth, registration,
                             send_message, sendpasswd, update_client)
from storage.models import Box, Client, Order, Storage

User._meta.get_field('email')._unique = True
from selfstorage.settings import BITLY_TOKEN
from storage.bitly import get_bitly_or_get_clicks_on_link
from storage.models import Client


def index(request):
    context = {}

    if 'message' in request.session and request.session['message']:
        context = {
            'message': request.session.get('message'),
        }
        request.session['message'] = ''

    elif 'EMAIL_CREATE' in request.POST:
        registration(request)
        return redirect('/')

    elif 'EMAIL' in request.POST:
        auth(request)
        return redirect('/')

    elif 'EMAIL_FORGET' in request.POST:
        sendpasswd(request)
        return redirect('/')
    elif 'BID_EMAIL' in request.POST:
        create_empty_order(request)
        return redirect('/')

    elif 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            }
    context = {
            'bit_link': get_bitly_or_get_clicks_on_link(request),
            }

    context['storages'] = Storage.objects.get_boxes()
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
    context['storages'] = Storage.objects.get_boxes()
    context['random_storage'] = random.choice(Storage.objects.get_boxes())
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
    message = ''
    if 'message' in request.session and request.session['message']:
        message = request.session.get('message')

        request.session['message'] = ''
    if 'PHONE_EDIT' in request.POST:
        update_client(request)
    if 'user_name' in request.session:
        client = Client.objects.get(user=request.user)
        orders = list(client.orders.all().prefetch_related('box'))
        context = {
            'username': request.session['user_name'],
            'client': client,
            'orders': orders,
            'message': message,
        }

    return render(request, 'my-rent.html', context=context)


def storages(request):
    context = {}
    if 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            'storages': Storage.objects.get_boxes(),
        }
    else:
        context = {
            'storages': Storage.objects.get_boxes(),
        }
    return render(request, 'storages.html', context=context)


def box_select(request, storage_id):
    context = {}
    boxes = Box.objects.filter(storage=storage_id, is_occupied=False).order_by('price')
    if 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            'boxes': boxes,
        }
    else:
        context = {
            'boxes': boxes,
        }
    return render(request, 'box-select.html', context=context)


def create_order(request, box_id):
    context = {}
    if 'user_name' in request.session:

        box = Box.objects.get(id=box_id)
        client = Client.objects.get(user=request.user)
        order = Order.objects.create(
            client=client, created_at=datetime.datetime.now(), box=box, price=box.price
        )
        Client.objects.filter(user=request.user).update(need_invoice=True)
        context = {
            'username': request.session['user_name'],
            'order': order,
        }

    return render(request, 'order_confirmation.html', context)


def storages(request):
    context = {}
    if 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            'storages': Storage.objects.get_boxes(),
        }
    else:
        context = {
            'storages': Storage.objects.get_boxes(),
        }
    return render(request, 'storages.html', context=context)


def box_select(request, storage_id):
    context = {}
    boxes = Box.objects.filter(storage=storage_id, is_occupied=False).order_by('price')
    if 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            'boxes': boxes,
        }
    else:
        context = {
            'boxes': boxes,
        }
    return render(request, 'box-select.html', context=context)


def create_order(request, box_id):
    context = {}
    if 'user_name' in request.session:

        box = Box.objects.get(id=box_id)
        client = Client.objects.get(user=request.user)
        order = Order.objects.create(
            client=client, created_at=datetime.datetime.now(), box=box, price=box.price
        )
        context = {
            'username': request.session['user_name'],
            'order': order,
        }

    return render(request, 'order_confirmation.html', context)



# def track_link_click(request):
#     link_name = 'https://github.com/morozgit/ClickCount/blob/master/main.py'
#     decoded_link_name = unquote(link_name)
#     print(decoded_link_name)

#     # Ваш код обработки, используя decoded_link_name

#     return render(request, 'track_link_click.html')