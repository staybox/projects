# coding: utf8
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    titles = ['Basilica', 'CIMDN', 'Nazareth_village']
    c = {'titles': titles}
    return render(request, 'index.html', c)


def pages(request, key):
    #titles = ['Basilica', 'CIMDN', 'Nazareth_village']
    c = {'titles': key}
    return render(request, 'pages.html', c)
