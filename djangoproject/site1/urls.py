from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^pages/(.+)$', views.pages, name='pages'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)