# coding: utf8
from django.shortcuts import render, redirect
from .models import Attractions, Towns, Orders
from django.http import HttpResponse
from django.template import RequestContext
from .forms import ContactForm


def index(request):
    all = Attractions.objects.filter(town='Nazareth')  # all attractions in Nazareth
    naz = Towns.objects.filter(name='Nazareth')  # only Nazareth
    c = {'data': naz, 'all': all}
    return render(request, 'pages.html', c)


def search(request):
    all = Attractions.objects.filter(town='Nazareth')  # all attractions in Nazareth
    naz = Towns.objects.filter(name='Nazareth')  # only Nazareth
    if 'q' in request.GET:
        r = request.GET['q']
        if r == '' or len(r) > 20:
            c = {'data': naz, 'error': True}
        else:
            all = all.filter(name__icontains=r)
            c = {'data': naz, 'all': all, 'search': r}
    else:
        c = {'data': naz, 'error': True}
    return render(request, 'pages.html', c)


def pages(request, name):
    data = Attractions.objects.filter(name=name)
    c = {'data': data}
    return render(request, 'pages.html', c)


def my_cart(request):
    d = request.session
    a = []
    for k, v in d.items():
        if '_session_expiry' not in k:
            a.append(k)
    a_str = ','.join(a)
    c = {'cart_list': a, 'a_str': a_str}
    return render(request, 'my_cart.html', c)


def add_to_cart(request, name):
    request.session.set_expiry(60)
    request.session[name] = 1
    data = Attractions.objects.filter(name=name)
    c = {'data': data}
    return render(request, 'pages.html', c)


def order(request):
    p = request.POST
    client_name = p['client_name']
    phone_number = p['phone_number']
    cart_list = p['cart_list']
    s = ContactForm({'client_name':client_name, 'phone_number':phone_number, 'order':cart_list})
    if s.is_valid():
        d = Orders(client_name=client_name, phone_number=phone_number, order=cart_list)
        d.save()
        data1 = [client_name, phone_number, cart_list]
        c = {'data1': data1}
    else:
        data1 = [s.errors]
        c = {'errors': data1}
    return render(request, 'congrats.html', c)
