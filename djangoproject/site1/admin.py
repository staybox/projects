from django.contrib import admin
from .models import Attractions


class AttractionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'wikipedia', 'tripadvisor', 'google_map', 'web_site')
    search_fields = ('name',)

admin.site.register(Attractions, AttractionsAdmin)