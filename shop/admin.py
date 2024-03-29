import re

from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import gettext_lazy as _
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import OrderItem, Order, PageText, PageTextGroup, Feedback, File


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    exclude = ('phone',)
    readonly_fields = ('price_admin',)
    extra = 0

    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        """
        Remove popup add/edit/delete icons by default for relation fields.
        """
        if db_field.is_relation:
            rel = db_field.related_model
            wrapped_widget = RelatedFieldWidgetWrapper(
                db_field.formfield().widget,
                rel,
                admin.site,
                can_add_related=False,
                can_change_related=False,
                can_delete_related=False
            )
            db_field.formfield().widget = wrapped_widget
            return db_field.formfield()
        return super(OrderItemInline, self).formfield_for_dbfield(db_field, **kwargs)


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price',)
    list_display = ('phone', 'status', 'address', 'delivery_date', 'delivery_time',
                    'first_name', 'total_price', 'payment')
    date_hierarchy = 'delivery_date'
    exclude = ('user',)
    inlines = (OrderItemInline,)


class PageTextFormset(BaseInlineFormSet):
    def clean(self):
        super(PageTextFormset, self).clean()
        names = [item['text_name'] for item in self.cleaned_data]
        if len(names) != len(set(names)):
            raise ValidationError(_('Text names must be unique'))
        for name in names:
            if not re.match(r"^[a-z0-9_]+$", name):
                raise ValidationError(_('Text name must consist of small letters and digits'))


class PageTextInline(admin.TabularInline):
    model = PageText
    formset = PageTextFormset
    list_display = ('page_name',)
    extra = 0
    min_num = 1


@admin.register(PageTextGroup)
class PageTextAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = (PageTextInline,)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    fields = ('created_at', 'phone')
    readonly_fields = fields
    list_display = ('created_at', 'phone')
    ordering = ('-created_at',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    fields = ('updated_at', 'name', 'file')
    readonly_fields = ('updated_at',)
    list_display = ('name', 'updated_at')
    ordering = ('-updated_at',)
