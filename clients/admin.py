from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from clients.models import Customer, Company
from shop.models import CustomerOrder, LegalOrder


class UserOrders(BaseInlineFormSet):
    def __init__(self, *args, **qwargs):
        super(UserOrders, self).__init__(*args, **qwargs)
        user = qwargs['instance']
        self.queryset = CustomerOrder.objects.filter(phone=user.phone)


class CompanyOrders(BaseInlineFormSet):
    def __init__(self, *args, **qwargs):
        super(CompanyOrders, self).__init__(*args, **qwargs)
        company = qwargs['instance']
        self.queryset = LegalOrder.objects.filter(company_id=company.id)


class OrderInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    exclude = ('phone',)

    def has_add_permission(self, request):
        return False


class CustomOrderInline(OrderInline):
    model = CustomerOrder
    formset = UserOrders
    readonly_fields = ('created_at', 'first_name', 'delivery_date', 'delivery_time', 'total_price')


class CompanyOrderInline(OrderInline):
    model = LegalOrder
    formset = CompanyOrders
    readonly_fields = ('created_at', 'delivery_date', 'total_price')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('phone', 'name', 'points')
    search_fields = ('phone', 'name')
    inlines = (CustomOrderInline,)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('unp', 'name', 'phone', 'email',
                    'payment', 'address_order',
                    'address_legal', 'contact_person', 'note',
                    )
    search_fields = ('unp', 'name', 'number', 'email',)

    inlines = (CompanyOrderInline,)