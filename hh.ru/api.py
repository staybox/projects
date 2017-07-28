# coding: utf8
import os
import requests
#import json
#import pdfkit


def urls():
    """
    Использует api hh.ru
    Печатает только вакансии с указанным телефоном с сайта hh.ru в pdf файл по запросу "Ежедневные выплаты",
    "Промоутер", "Уборщик территорий", "Подсобный рабочий"
    """
    all_textes = []
    line = '\n'+'-'*100
    numb = 1 #порядковый номер вакансии

    texts = ['%D0%B5%D0%B6%D0%B5%D0%B4%D0%BD%D0%B5%D0%B2%D0%BD%D1%8B%D0%B5+%D0%B2%D1%8B%D0%BF%D0%BB%D0%B0%D1%82%D1%8B',
             '%D0%A0%D0%B0%D0%B7%D0%B4%D0%B0%D1%87%D0%B0+%D0%BB%D0%B8%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%BA',
             '%D0%9F%D0%BE%D1%81%D0%B0%D0%B4%D0%BA%D0%B0+%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D0%B5%D0%B2',
             '+%D0%9F%D0%BE%D0%B4%D1%81%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9+%D1%80%D0%B0%D0%B1%D0%BE%D1%87%D0%B8%D0%B9']
             #ежедневные выплаты, Промоутер, Уборщик территорий, Подсобный рабочий
    for i in texts:
        url = 'https://api.hh.ru/vacancies?order_by=publication_time&specialization=3.509&specialization=29.555&' \
              'specialization=29.554&specialization=29.556&specialization=29.510&specialization=29.512&' \
              'specialization=29.515' \
              '&specialization=29.558&specialization=29.517&specialization=29.559&specialization=29.514&' \
              'specialization=29.583&specialization=29.581&specialization=29.588&specialization=29.561&' \
              'specialization=29.544' \
              '&specialization=29.545&specialization=29.542&specialization=29.540&specialization=29.541&' \
              'specialization=29.548&specialization=29.495&schedule=fullDay&schedule=shift&schedule=flexible&' \
              'schedule=flyInFlyOut&enable_snippets=true&area=1&text={0}&clusters=true&no_magic=true&employment=full' \
              '&employment=part&employment=project&label=not_from_agency&experience=noExperience'.format(i)
        out_list = parse_data(url)
        for k in out_list:
            order = '{0}. | '.format(numb)
            numb += 1
            k = order + k
            all_textes.append(k)
    all_textes.append(line)
    make_pdf(all_textes, 1) # 1 = print only once on a list


def parse_data(url):
    headers = {'User-Agent': 'api-test-agent'}
    r = requests.get(url, headers=headers)
    a = r.json()["items"]
    b = len(a)
    out_list = []
    limit = 10 #ограничение количества вакансий одной профессии
    for i in range(b):
        if i <= limit:
            n = a[i]
            name = n['name']
            url_vac = n['url']
            employer = n['employer']['name']
            vac = requests.get(url_vac, headers=headers).json()
            contacts = vac["contacts"]
            #print n['address']
            #http://jsonviewer.stack.hu/
            try:
                try:
                    metro = n['address']['metro']['station_name']
                    metro = metro.encode('utf-8')
                    metro = ' | Метро: {0}'.format(metro)
                except:
                    metro = '' #если не указана станция метро, то ничего не печатаем
                #print metro
                phones = contacts['phones'][0]
                country = phones['country']
                code = phones['city']
                number = phones['number']
                phone = ' | Телефон:+{0}({1}){2}'.format(country, code, number)
                name = name.encode('utf-8')
                employer = employer.encode('utf-8')
                out = name + ' | Компания: ' + employer + phone + metro + ' |'# + '<br>'
                #print out
                out_list.append(out)
            except:
                pass
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
    print ('api.py finished the parsing')
    #pdfkit.from_file('job.html', 'job.pdf')
    #os.remove('job.html')


if __name__ == '__main__':
    urls()
