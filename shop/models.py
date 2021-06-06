import logging

from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _, pgettext_lazy

from accounts.models import User
from catalog.models import Pizza, Size
import telebot

from .settingTelegramBot import *

log = logging.getLogger(__name__)


class LegalOrder(models.Model):
    DELIVERY_TIME_CHOICES = [
        (0, '09-10'),
        (1, '10-11'),
        (2, '11-12'),
        (3, '12-13'),
        (4, '13-14'),
        (5, '14-15'),
        (6, '15-16'),
        (7, '16-17'),
        (8, '17-18'),
        (9, '18-18.30'),
    ]
    PAYMENT_CHOICES = [
        (0, _('Cash')),
        (1, _('Card')),
        (2, _('Online')),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    delivery_date = models.DateField(verbose_name=_('Delivery date'))
    delivery_time = models.SmallIntegerField(
        choices=DELIVERY_TIME_CHOICES,
        verbose_name=_('Delivery time'),
    )
    comment = models.TextField(max_length=100, verbose_name=_('Comment'), blank=True, null=True)
    payment = models.SmallIntegerField(
        choices=PAYMENT_CHOICES,
        verbose_name=_('Payment method'),
    )
    status = models.BooleanField(default=0, verbose_name=_('Payment confirmed'))

    class Meta:
        verbose_name = _('Legal order')
        verbose_name_plural = _('Legal orders')


class Order(models.Model):
    DELIVERY_TIME_CHOICES = [
        (0, '09-10'),
        (1, '10-11'),
        (2, '11-12'),
        (3, '12-13'),
        (4, '13-14'),
        (5, '14-15'),
        (6, '15-16'),
        (7, '16-17'),
        (8, '17-18'),
        (9, '18-18.30'),
    ]
    PAYMENT_CHOICES = [
        (0, _('Cash')),
        (1, _('Card')),
        (2, _('Online')),
    ]
    phone = models.CharField(max_length=10, verbose_name=_('Phone'))
    first_name = models.CharField(max_length=100, verbose_name=pgettext_lazy('Order|Name', 'Order'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    delivery_date = models.DateField(verbose_name=_('Delivery date'))
    delivery_time = models.SmallIntegerField(
        choices=DELIVERY_TIME_CHOICES,
        verbose_name=_('Delivery time'),
    )
    address = models.CharField(max_length=100, verbose_name=_('Address'))
    comment = models.TextField(max_length=100, verbose_name=_('Comment'), blank=True, null=True)
    payment = models.SmallIntegerField(
        choices=PAYMENT_CHOICES,
        verbose_name=_('Payment method'),
    )
    status = models.BooleanField(default=0, verbose_name=_('Payment confirmed'))

    def total_price(self):
        return sum([item.price for item in self.orderitem_set.all()])

    total_price.allow_tags = True

    total_price.short_description = _('Total price')

    def __str__(self):
        return f"№ {self.id}"

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

# Email
# def order_update(sender, instance, created, **kwargs):
#     if created:
#         try:
#             subject = 'Новый заказ'
#             from_email = 'Печорин'
#             to = 'zakaz_pechorin@mail.ru'
#             site = Site.objects.get()
#             text_content = f'{site.domain}/admin/shop/order/{instance.id}/change'
#             html_content = f'<a href={site.domain}/admin/shop/order/{instance.id}/change>Новый заказ</a>'
#             # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#             # msg.attach_alternative(html_content, "text/html")
#             # msg.send(fail_silently=False)
#             send_mail(subject, text_content, from_email, [to], fail_silently=False, html_message=html_content)
#         except Exception as ex:
#             log.error(ex)

ID_CHAT = '1413258846'
bot = telebot.TeleBot(TOKEN_BOT, parse_mode='HTML')


def order_update(sender, instance, created, **kwargs):
    if created:
        try:
            subject = 'Новый заказ'
            site = Site.objects.get()
            text_content = f'{site.domain}/admin/shop/order/{instance.id}/change'
            HTML_Button = f'<a href="{site.domain}/admin/shop/order/{instance.id}/change" >Новый заказ</a>'
            for admin in TelegramBot.objects.all():
                bot.send_message(admin.idChat, subject + "\n" + text_content + "\n" + HTML_Button)
        except Exception as ex:
            log.error(ex)


post_save.connect(order_update, sender=Order)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Order'))
    item = models.ForeignKey(Pizza, on_delete=models.DO_NOTHING, verbose_name=_('Item'))
    size = models.CharField(max_length=100, choices=Size.CHOICES, verbose_name=_('Size'))
    quantity = models.PositiveSmallIntegerField(verbose_name=_('Quantity'))

    @property
    def price(self):
        return self.item.sizes.get(type=self.size).price * self.quantity

    "Property admin panel translation"

    def price_admin(self):
        return self.price

    price_admin.short_description = _('Price')

    def __str__(self):
        return f""

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class PageTextGroup(models.Model):
    page_name = models.CharField(max_length=100, verbose_name=_('Page name'))
    title = models.CharField(max_length=100, verbose_name=_('Title'))

    def __str__(self):
        return self.page_name

    class Meta:
        verbose_name = _('Page text')
        verbose_name_plural = _('Page texts')


class PageText(models.Model):
    text = models.TextField(max_length=2000, verbose_name=_('Text'))
    text_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Text name'))
    group = models.ForeignKey(PageTextGroup, on_delete=models.CASCADE, related_name='texts')

    def __str__(self):
        return f""

    class Meta:
        verbose_name = _('Page text')
        verbose_name_plural = _('Page texts')


class TelegramBot(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    idChat = models.CharField(max_length=255, verbose_name='ID чата')

    class Meta:
        verbose_name = 'Модератор'
        verbose_name_plural = 'Модераторы'

    def __str__(self):
        return self.name
