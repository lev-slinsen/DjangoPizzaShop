"""
Accounts models.
"""
import re

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.signals import user_logged_in
from django.db.models import signals
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _, pgettext_lazy


class UserManager(BaseUserManager):
    """
    Custom user manager.
    """
    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given phone and password.
        """
        if not phone:
            raise ValueError('The given phone must be set')
        phone = self.model.normalize_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """
        Override `django.contrib.auth.models.UserManager.create_superuser` to support `phone` as unique identifier.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model.
    """
    phone = models.CharField(max_length=100, unique=True, verbose_name=_('Phone'))
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    first_name = models.CharField(max_length=30, verbose_name=pgettext_lazy('User|Name', 'Name'))
    language = models.CharField(max_length=20, choices=settings.LANGUAGES, default='ru', verbose_name=_('Language'))

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

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


@receiver(signals.post_save, sender=User)
def email(sender, instance, **kwargs):
    if instance.email:
        send_mail(
            'Subject',
            'Message',
            'DjangoPizzaShop',
            [instance.email],
            fail_silently=False,
        )
