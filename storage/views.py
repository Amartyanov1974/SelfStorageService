from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings

from storage.models import Client
from storage.actions import auth, registration, deauth, send_message

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


def my_rent(request):
    context = {}
    if 'user_name' in request.session:
        client = Client.objects.get(user=request.user)
        context = {
            'username': request.session['user_name'],
            'email': client.user_email,
            }
    return render(request, 'my-rent.html', context=context)


