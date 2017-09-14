from django.contrib import admin
from .models import Attractions, Towns


@admin.register(Attractions, Towns)
class DefaultAdmin(admin.ModelAdmin):
    pass
# class AttractionsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'text', 'wikipedia', 'tripadvisor', 'google_map', 'web_site', 'town')
#
#
# class TownsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'text', 'wikipedia', 'tripadvisor', 'google_map')
#     search_fields = ('name',)
#
