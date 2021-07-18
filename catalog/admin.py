from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import PromoCodeGroup


from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import Category, Pizza, Size, Price


class SizeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(SizeInlineFormSet, self).clean()
        actives = [item['active'] for item in self.cleaned_data]
        print(actives)
        if len(list(filter(lambda x: x, actives))) != 1:
            raise ValidationError('Select 1 active size')

# class SizeInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super(SizeInlineFormSet, self).clean()
#         actives = 0
#         pizza = self.form.clean(self)
#         id = 0
#         for i in self.forms:
#             if pizza[id].get('active') is True:
#                 actives += 1
#             id += 1
#         if actives != 1:
#             raise ValidationError('Select 1 active size')


class SizeInline(admin.TabularInline):
    model = Size
    formset = SizeInlineFormSet
    extra = 0
    max_num = 2


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    readonly_fields = ('price',)
    list_display = ('name', 'price')


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'content', 'description', 'category', 'photo')
    list_filter = ('category__name',)

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    inlines = (SizeInline,)


class PromoCodeBatchAdmin(admin.ModelAdmin):
    model = PromoCodeGroup


admin.site.register(Category)
# admin.site.register(PromoCodeGroups)
admin.site.unregister(Group)
