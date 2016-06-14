# coding: utf8
import os
import requests
import json
import pdfkit


def urls():
    """
    Использует api hh.ru
    Печатает только вакансии с указанным телефоном с сайта hh.ru в pdf файл по запросу "Ежедневные выплаты"
    """
    url = 'https://api.hh.ru/vacancies?order_by=publication_time&specialization=3.509&specialization=29.555&specialization=29.554&specialization=29.556&specialization=29.510&specialization=29.512&specialization=29.515&specialization=29.558&specialization=29.517&specialization=29.559&specialization=29.514&specialization=29.583&specialization=29.581&specialization=29.588&specialization=29.561&specialization=29.544&specialization=29.545&specialization=29.542&specialization=29.540&specialization=29.541&specialization=29.548&specialization=29.495&schedule=fullDay&schedule=shift&schedule=flexible&schedule=flyInFlyOut&enable_snippets=true&area=1&text=%D0%B5%D0%B6%D0%B5%D0%B4%D0%BD%D0%B5%D0%B2%D0%BD%D1%8B%D0%B5+%D0%B2%D1%8B%D0%BF%D0%BB%D0%B0%D1%82%D1%8B&clusters=true&no_magic=true&employment=full&employment=part&employment=project&label=not_from_agency'
    parse_data(url)
    out_list = parse_data(url)
    make_pdf(out_list, 7)


def parse_data(url):
    headers = {'User-Agent': 'api-test-agent'}
    r = requests.get(url, headers=headers)
    a = r.json()["items"]
    b = len(a)
    k = 1
    line = '\n'+'-'*170
    out_list = []
    for i in range(b):
        n = a[i]
        name = n['name']
        url_vac = n['url']
        employer = n['employer']['name']
        vac = requests.get(url_vac, headers=headers).json()
        contacts = vac["contacts"]
        if contacts is not None:
            phones = contacts['phones'][0]
            country = phones['country']
            code = phones['city']
            number = phones['number']
            phone = ' | Телефон:+{0}({1}){2} |'.format(country, code, number)
            order = '{0}. | '.format(k)
            k += 1
            name = name.encode('utf-8')
            employer = employer.encode('utf-8')
            out = order + name + ' | Название компании: ' + employer + phone
            out_list.append(out)
    out_list.append(line)
    return out_list


def make_pdf(out_list, n):
    f = open('job.html', 'w')
    tags_1 = '<!DOCTYPE html><html><head><meta charset="utf-8"><h1>ВАКАНСИИ</h1></head><body>'
    tags_2 = '</body></html>'
    f.write(tags_1)
    for k in range(n):
        for i in out_list:
            f.write(i+'<br>')
        f.write('<br>')
    f.write(tags_2)
    f.close()
    pdfkit.from_file('job.html', 'job.pdf')
    os.remove('job.html')


if __name__ == '__main__':
    urls()
