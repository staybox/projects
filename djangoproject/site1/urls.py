from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/$', views.search, name='search'),
    url(r'^pages/(.+)$', views.pages, name='pages'),
    url(r'^my_cart/$', views.my_cart),
    url(r'^add_to_cart/(.+)$', views.add_to_cart),
    url(r'^order/$', views.order),
    url(r'^$', views.index, name='index'),
]
