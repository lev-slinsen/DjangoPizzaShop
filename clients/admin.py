from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from clients.models import Customer, Company
from shop.models import Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('phone', 'name', 'points')
    search_fields = ('phone', 'name', 'email')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('unp', 'name', 'address_legal', 'address_order')
    search_fields = ('unp', 'name')
