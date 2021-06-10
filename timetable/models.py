from django.db import models
from django.utils.translation import gettext_lazy as _, pgettext_lazy


class Date(models.Model):
    date = models.DateField(unique=True, verbose_name=_('Date'))

    class Meta:
        verbose_name = pgettext_lazy('Meta|Date', 'Date')
        verbose_name_plural = pgettext_lazy('Meta|Dates', 'Dates')

    def __str__(self):
        return f"{self.date}"
