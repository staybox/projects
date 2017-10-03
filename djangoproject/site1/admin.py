from django.contrib import admin
from .models import Attractions, Towns, Orders


class AttractionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'wikipedia', 'tripadvisor', 'google_map', 'web_site', 'town')
    search_fields = ('name',)


class TownsAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'wikipedia', 'tripadvisor', 'google_map')
    search_fields = ('name',)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone_number', 'order', 'order_date')
    search_fields = ('client_name',)


admin.site.register(Attractions, AttractionsAdmin)
admin.site.register(Towns, TownsAdmin)
admin.site.register(Orders, OrdersAdmin)
