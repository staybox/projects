from site1.models import Attractions


def aaa():
    a1 = Attractions(name='Basilica',
                         wikipedia='https://en.wikipedia.org/wiki/Basilica_of_the_Annunciation',
                         tripadvisor='https://www.tripadvisor.com/Attraction_Review-g297758-d379356-Reviews-The_Church_of_the_Annunciation-Nazareth_Galilee_Northern_District.html',
                         google_map='https://goo.gl/maps/v1PETNrQZVm',
                         web_site='http://www.nazareth-en.custodia.org/default.asp')
    a1.save()

    a2 = Attractions(name='CIMDN',
                         wikipedia='',
                         tripadvisor='https://www.tripadvisor.fr/Attraction_Review-g297758-d3626143-Reviews-International_Center_Mary_of_Nazareth-Nazareth_Galilee_Northern_District.html',
                         google_map='https://goo.gl/maps/j1wFPa7dFuG2',
                         web_site='https://il.chemin-neuf.org/en/home/locations/mary-of-nazareth-international-center')
    a2.save()

    a3 = Attractions(name='Nazareth_village',
                         wikipedia='https://en.wikipedia.org/wiki/Nazareth_Village',
                         tripadvisor='https://www.tripadvisor.com/Attraction_Review-g297758-d1627228-Reviews-Nazareth_Village-Nazareth_Galilee_Northern_District.html',
                         google_map='https://goo.gl/maps/bSSZbdUdTqk',
                         web_site='www.nazarethvillage.com/')
    a3.save()

    a4 = Attractions(name='Mount_Tabor',
                         wikipedia='https://en.wikipedia.org/wiki/Mount_Tabor',
                         tripadvisor='https://www.tripadvisor.com/Attraction_Review-g1650028-d1753722-Reviews-Mount_Tabor-Kfar_Tavor_Galilee_Northern_District.html',
                         google_map='https://goo.gl/maps/bTXsf6vU9U52',
                         web_site='')
    a4.save()