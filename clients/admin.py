from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from clients.models import Customer, Company
from shop.models import Order


# class OrderInline(admin.TabularInline):
#     model = Order
#     formset = UserOrders
#     extra = 0
#     show_change_link = True
#     readonly_fields = ('created_at', 'first_name', 'delivery_date', 'delivery_time', 'total_price')
#     exclude = ('phone',)
#
#     def has_add_permission(self, request):
#         return False


class CustomerAdmin(admin.ModelAdmin):
    """
    User admin.
    """
    fields = ()

    list_display = ('phone', 'first_name', 'point')
    search_fields = ('phone', 'name', 'email')

    # inlines = (OrderInline,)


class CompanyAdmin(admin.ModelAdmin):
    """
    User admin.
    """
    fields = ()

    list_display = ('unp', 'name', 'legal_address', 'address_order')
    search_fields = ('unp', 'name')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Company, CompanyAdmin)
