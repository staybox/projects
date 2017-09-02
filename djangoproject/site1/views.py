# coding: utf8
from django.shortcuts import render
from .models import Attractions


def index(request):
    titles = ['Basilica', 'CIMDN', 'Nazareth_village', 'Mount_Tabor']
    c = {'titles': titles}
    return render(request, 'index.html', c)


def pages(request, name):
    data = Attractions.objects.filter(name=name)
    c = {'data': data}
    return render(request, 'pages.html', c)