"""
Catalogue models.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.utils.timezone import localtime, now


class Category(models.Model):
    """
    Category model.
    """
    name = models.CharField(verbose_name=pgettext_lazy('Category|Name', 'Name'), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Pizza(models.Model):
    """
    Pizza model.
    """
    name = models.CharField(verbose_name=pgettext_lazy('Pizza|Name', 'Name'), max_length=100)
    content = models.CharField(verbose_name=_('Content'), max_length=100)
    description = models.TextField(verbose_name=_('Description'))
    category = models.ManyToManyField(Category, verbose_name=_('Category'))
    photo = models.ImageField(upload_to='images/', verbose_name=_('Image'))

    class Meta:
        verbose_name = _("Pizza")
        verbose_name_plural = _("Pizzas")

    @property
    def categories_display(self):
        return ' '.join(str(cat) for cat in self.category.all())

    def __str__(self):
        #    return "name = {}, size = {}".format(self.name, self.size)
        #    return "name = %s, size = %s" % (self.name, self.size)
        return f"{self.name}"

    @property
    def default_price(self):
        active = self.sizes.filter(active=True).first()
        if not active:
            raise Exception(f'Active size not set. {self}')
        return active.price


class Size(models.Model):
    CHOICES = (
        ('small', _('Small')),
        ('large', _('Large')),
        ('none', _('None')),
    )
    type = models.CharField(max_length=20, choices=CHOICES, verbose_name=_('Type'))
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_('Price'))
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='sizes', verbose_name=_('Pizza'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))

    class Meta:
        verbose_name = _("Size")
        verbose_name_plural = _("Sizes")

    def __str__(self):
        return f""


class PromoCodeGroup(models.Model):
    name = models.CharField(max_length=10, verbose_name=_('Name'))
    disc_percent = models.IntegerField(verbose_name=_('Discount percent'), blank=True, null=True)
    disc_value = models.IntegerField(verbose_name=_('Discount value'), blank=True, null=True)
    start_date = models.DateField(verbose_name=_('Start date'), default=now)
    expiration_date = models.DateField(verbose_name=_('Expiration date'), blank=True, null=True, default=None)

    class Meta:
        verbose_name_plural = _('Promo code groups')


class PromoCode(models.Model):
    code = models.CharField(max_length=10, verbose_name=_('Code'))
    group = models.ForeignKey(PromoCodeGroup, on_delete=models.CASCADE, related_name='codes')


class Price(models.Model):
    name = models.CharField(max_length=15, verbose_name=_('Name'))
    # price = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_('Price'))
    product = models.ManyToManyField(Pizza)

    def price(self):
        return sum(item.sizes.get().price for item in self.product.all())

    def __str__(self):
        return self.name
