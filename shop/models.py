import os, requests

from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from dotenv import load_dotenv
from django.conf import settings

from accounts.models import User
from catalog.models import Pizza, Size

load_dotenv()


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
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
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


def send_email_notification(sender, instance, created, **kwargs):
    email = os.environ.get('NOTIFICATIONS_EMAIL', None)
    if email and created and not settings.ENABLE_LOGGING:
        site = Site.objects.get()
        if sender == Order:
            subject = 'Новый заказ'
            html_content = f'''
                Новый заказ
                {site.domain}/admin/shop/order/{instance.id}/change
                Телефон: {instance.phone}
                Имя: {instance.first_name}
                Дата: {instance.delivery_date}
                Время: {instance.delivery_time}
                Адрес: {instance.address}
                Оплата: {instance.payment}
                Сумма: {instance.total_price()}
                '''
        elif sender == Feedback:
            subject = 'Обратный звонок'
            html_content = f'''
                Запрос на обратный звонок на телефон {instance.phone}
                {site.domain}/admin/shop/feedback/{instance.id}/change
                '''
        else:
            return

        return requests.post(
            os.getenv('MAILGUN_URL'),
            auth=("api", os.getenv('MAILGUN_API_KEY')),
            data={"from": "Автоматическое уведомление <postmaster@sandbox24e837ccfffa4f42a597feb45d64af9d.mailgun.org>",
                  "to": os.environ.get('NOTIFICATIONS_EMAIL', None),
                  "subject": subject,
                  "text": html_content})
    pass


post_save.connect(send_email_notification, sender=Order)


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


class Feedback(models.Model):
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.phone


post_save.connect(send_email_notification, sender=Feedback)


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    def __str__(self):
        return self.name

    def url(self):
        return self.file.url
