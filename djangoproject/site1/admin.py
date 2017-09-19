from django.contrib import admin
from .models import Attractions, Towns


class AttractionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'wikipedia', 'tripadvisor', 'google_map', 'web_site', 'town')
    search_fields = ('name',)


class TownsAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'wikipedia', 'tripadvisor', 'google_map')
    search_fields = ('name',)


admin.site.register(Attractions, AttractionsAdmin)
admin.site.register(Towns, TownsAdmin)
