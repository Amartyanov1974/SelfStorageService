from django.shortcuts import render


def index(request):
    # if 'user_name' in request.session:
        # context = {
            # 'username': request.session['user_name'],
            # }
        # return render(request, 'index.html', context=context)
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
