import string
import random
from random import choice
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings

from storage.models import Client, Order


User._meta.get_field('email')._unique = True

def auth(request):
    """ Авторизация пользователя

    До авторизации request.user="AnonymousUser"
    После авторизации request.user=user(email)
    """
    username = request.POST['EMAIL']
    password = request.POST['PASSWORD']
    try:
        user = authenticate(username=username, password=password)
    except:
        user = None
    if not user:
        request.session['message'] = 'Ошибка авторизации'
        return 0
    login(request, user)
    user = User.objects.get(username=username)
    request.session['user_name'] = user.first_name
    return 0


def registration(request):
    """Регистрация

    Сохраняем имя в first_name объекта user,
    почту используем в качестве логина
    Проверяем подтвержение пароля и уникальность логина (почты)
    """

    first_name = request.POST['NAME_CREATE']
    username = request.POST['EMAIL_CREATE']
    email = request.POST['EMAIL_CREATE']
    password = request.POST['PASSWORD_CREATE']
    passwordconfirm = request.POST['PASSWORD_CONFIRM']

    if password != passwordconfirm:
        request.session['message'] = 'Пароли не совпадают'
        return 0

    try:
        user = User.objects.create_user(
            first_name=first_name,
            username=username,
            password=password,
            email=email,
        )
        client = Client.objects.create(
            user=user,
        )
    except:
        request.session['message'] =  'Пользователь с такой почтой существует'
        return 0
    login(request, user)
    request.session['user_name'] = first_name
    return 0


def deauth(request):
    logout(request)
    #request.session.clear()
    request.session.pop('user_name', None)
    return redirect('/')


def send_message(*args):
    """
    Здесь будет код
    """
    return redirect('admin/storage/order')

def send_check(*args):
    """
    Здесь будет код
    """
    return redirect('admin/storage/client')


def create_empty_order(request):
    first_name = request.POST['BID_NAME']
    username = request.POST['BID_EMAIL']
    email = request.POST['BID_EMAIL']
    sizes = request.POST['BID_SIZES']
    try:
        chars = f'{string.ascii_letters}{string.digits}'
        password = ''.join([choice(chars) for i in range(7)])

        user = User.objects.create_user(
            first_name=first_name,
            username=username,
            password=password,
            email=email,
        )
        client = Client.objects.create(
            user=user,
        )
        order =Order.objects.create(client=client,
                                    size=sizes)
    except:
        request.session['message'] =  'Пользователь с такой почтой существует, авторизуйтесь'
        return 0
    request.session['message'] =  'Ваша заявка отправлена, с Вами свяжутся'
    return 0


def create_client(request):
    first_name = request.POST['NAME_CREATE']
    username = request.POST['EMAIL_CREATE']
    email = request.POST['EMAIL_CREATE']
    try:
        chars = f'{string.ascii_letters}{string.digits}'
        password = ''.join([choice(chars) for i in range(7)])

        user = User.objects.create_user(
            first_name=first_name,
            username=username,
            password=password,
            email=email,
        )
        client = Client.objects.create(
            user=user,
        )
    except:
        return redirect('admin/storage/client')
    return redirect('admin/storage/client')


def sendpasswd(request):
    """Генерация пароля и отправка по почте

    Для работы функции отправки пароля по почте необходимо в .env
    занести следующие параметры:
    EMAIL_HOST
    DEFAULT_FROM_EMAIL
    EMAIL_PORT
    EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD
    EMAIL_USE_SSL
    Подробности: https://djangodoc.ru/3.2/topics/email/
    """
    email = request.POST['EMAIL_FORGET']
    try:
        user = User.objects.get(email=email)
    except:
        request.session['message'] = 'Пользователь с такой почтой не зарегистрирован'
        return 0
    chars = f'{string.ascii_letters}{string.digits}'
    new_passwd = ''.join([choice(chars) for i in range(7)])
    try:
        user.set_password(new_passwd)
        user.save()
        send_mail(
            'Новый пароль от SelfService',
            f'Ваш новый пароль: {new_passwd}',
            '',
            [email,],
            fail_silently=False,
        )
        request.session['message'] = 'Пароль выслан на вашу почту'
        return 0
    except:
        request.session['message'] = 'Сбой отправки почты'
        return 0
    return 0


def update_client(request):
    address = request.POST['ADDRESS_EDIT']
    phonenumber = request.POST['PHONE_EDIT']
    client, created = Client.objects.update_or_create(
        user=request.user,
        defaults={'address': address, 'phonenumber': phonenumber})
    return 0


def need_call(request):
    Client.objects.filter(user=request.user).update(need_call=True)
    request.session['message'] =  'В ближайшее врямя Вам перезвонят'
    return redirect('my_rent')


def need_invoice(request):
    Client.objects.filter(user=request.user).update(need_invoice=True)
    request.session['message'] =  'В ближайшее врямя Вам вышлют счет на E-mail'
    return redirect('my_rent')
