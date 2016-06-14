# coding: utf8
import os
import urllib2
import pdfkit


def dwld_txt():
    """
    Скачивает страницы сайта литургической тетрадки за месяц с claret.ru и создаёт pdf из этих страниц
    """
    url_p1 = 'http://claret.ru/liturgy/lb'
    url_p2 = '201608'
    url_p3_day = 1
    url_p4 = '.htm'

    f = open('text.html', 'w')
    while url_p3_day <= 31:
        if url_p3_day < 10:
            url_p3_day = '0' + str(url_p3_day)
        url_p3 = str(url_p3_day)
        url = url_p1 + url_p2 + url_p3 + url_p4
        s = urllib2.urlopen(url)
        s1 = s.read()
        s2 = s1.replace('<h1>ЛИТУРГИЧЕСКАЯ ТЕТРАДКА</h1>', '<br><br>')
        f.write(s2)
        url_p3_day = int(url_p3_day) + 1
    f.close()
    #pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')
    pdfkit.from_file('text.html', 'liturgy.pdf')
    os.remove('text.html')


if __name__ == '__main__':
    dwld_txt()
