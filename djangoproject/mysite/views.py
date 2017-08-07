# coding: utf8
from django.http import HttpResponse


def index(request):
    out = '<a href="job.html">Скачать вакансии</a>'
    return HttpResponse(out)


def vac_list(request):
    my_file = open('/home/allexeyv/projects/hh.ru/job.html','rb').read()
    #my_file = open('/home/ccninfo/Documents/projects/hh.ru/job.html','rb').read()
    return HttpResponse(my_file, content_type = "text/html")