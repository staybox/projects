# coding: utf8
from django.http import HttpResponse


def index(request):
    out = '<a href="job.pdf">Скачать вакансии</a>'
    return HttpResponse(out)


def pdf(request):
    my_file = open('/home/allexeyv/projects/hh.ru/job.pdf','rb').read()
    return HttpResponse(my_file, content_type = "application/pdf")