from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in


class User(models.Model):
    """
    Custom user model.
    """
    phone = models.CharField(max_length=100, unique=True, verbose_name=_('Phone'))
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    first_name = models.CharField(max_length=30, verbose_name=pgettext_lazy('User|Name', 'Name'))
    language = models.CharField(max_length=20, choices=settings.LANGUAGES, default='ru', verbose_name=_('Language'))
    point = models.IntegerField(default=0, verbose_name=_('Point'))

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.phone

    @classmethod
    def normalize_phone(cls, phone):
        """
        Remove extra spaces and non-digit chars from phone.
        """
        _normalize_phone = re.compile(r'(\s{2,}|[a-zA-Z]+)').sub
        return _normalize_phone('', phone)


@receiver(user_logged_in)
def lang(sender, **kwargs):
    lang_code = kwargs['user'].language
    kwargs['request'].session['django_language'] = lang_code