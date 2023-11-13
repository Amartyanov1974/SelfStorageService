from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail

from django.conf import settings


def index(request):
    for key, value in request.POST.items():
        print(f'Key: {key}')

        print(f'Value: {value}')
    if 'user_name' in request.session:
        context = {
            'username': request.session['user_name'],
            }
        return render(request, 'index.html', context=context)
    return render(request, 'index.html')


def faq(request):
    # if 'user_name' in request.session:
        # context = {
            # 'username': request.session['user_name'],
            # }
        # return render(request, 'index.html', context=context)
    return render(request, 'faq.html')


def boxes(request):
    # if 'user_name' in request.session:
        # context = {
            # 'username': request.session['user_name'],
            # }
        # return render(request, 'index.html', context=context)
    return render(request, 'boxes.html')


def my_rent(request):
    # if 'user_name' in request.session:
        # context = {
            # 'username': request.session['user_name'],
            # }
        # return render(request, 'index.html', context=context)
    return render(request, 'my-rent.html')


def my_rent_empty(request):
    # if 'user_name' in request.session:
        # context = {
            # 'username': request.session['user_name'],
            # }
        # return render(request, 'index.html', context=context)
    return render(request, 'my-rent-empty.html')


# def registration(request):
    # """Регистрация

    # Сохраняем имя в first_name объекта user,
    # почту используем в качестве логина
    # Проверяем подтвержение пароля и уникальность логина (почты)
    # """
    # #if request.method == 'POST': # and 'username' in request.POST:
    # for key, value in request.POST.items():
        # print(f'Key: {key}')

        # print(f'Value: {value}')

        # first_name = request.POST['username']
        # username = request.POST['email']
        # email = request.POST['email']
        # password = request.POST['passwd']
        # passwordconfirm = request.POST['passwdconfirm']
        # if password != passwordconfirm:
            # request.session['message'] = 'Пароли не совпадают'
            # return redirect('registration_message')
        # try:
            # user = authenticate(username=username, password=password)
        # except:
            # user=None
        # if not user:
            # try:
                # user = User.objects.create_user(
                    # first_name=first_name,
                    # username=username,
                    # password=password,
                    # email=email,
                # )
                # client = Client.objects.create(
                    # user=user,
                # )
            # except:
                # request.session['message'] =  'Пользователь с такой почтой существует'
                # return redirect('registration_message')
        # login(request, user)
        # request.session['user_name'] = first_name
        # return redirect('/')

    # return render(request, 'index.html' )
