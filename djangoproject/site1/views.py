# coding: utf8
from django.shortcuts import render
from .models import Attractions, Towns
from django.http import HttpResponse


def index(request):
    all = Attractions.objects.filter(town='Nazareth') # all attractions in Nazareth
    naz = Towns.objects.filter(name='Nazareth') # only Nazareth
    if 'q' in request.GET:
        r = request.GET['q']
        all = all.filter(name__icontains=r)
        c = {'data': naz, 'all': all, 'search': r}
    else:
        c = {'data': naz, 'all': all}
    return render(request, 'pages.html', c)


def pages(request, name):
    data = Attractions.objects.filter(name=name)
    c = {'data': data}
    return render(request, 'pages.html', c)
