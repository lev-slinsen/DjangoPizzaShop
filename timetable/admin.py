from django.contrib import admin
from .models import Date


class DateAdmin(admin.ModelAdmin):
    model = Date


admin.site.register(Date, DateAdmin)
