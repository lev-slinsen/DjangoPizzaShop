from django.db import models


class Company(models.Model):
    PAYMENT_CHOICES = [
        (0, 'Cash'),
        (1, 'Card'),
        (2, 'Online'),
    ]
    unp = models.CharField(max_length=255, verbose_name="UNP")
    name = models.CharField(max_length=255, verbose_name="Name")
    address_legal = models.CharField(max_length=255, verbose_name="Legal address")
    address_order = models.CharField(max_length=255, verbose_name="Delivery address")
    contact_person = models.CharField(max_length=50, verbose_name="The contact person")
    phone = models.CharField(max_length=25, unique=True, verbose_name="Number")
    note = models.TextField(max_length=2000, verbose_name="Note")
    email = models.CharField(max_length=50, verbose_name="Email")
    payment = models.SmallIntegerField(
        choices=PAYMENT_CHOICES,
        verbose_name="Payment format",
    )

    @classmethod
    def normalize_phone(cls, phone):
        _normalize_phone = re.compile(r'(\s{2,}|[a-zA-Z]+)').sub
        return _normalize_phone('', phone)


class Customer(models.Model):
    phone = models.CharField(max_length=100, unique=True, verbose_name='Phone')
    name = models.CharField(max_length=30, verbose_name='Name')
    points = models.IntegerField(default=0, verbose_name='Point')

    def __str__(self):
        return self.name

    @classmethod
    def normalize_phone(cls, phone):
        _normalize_phone = re.compile(r'(\s{2,}|[a-zA-Z]+)').sub
        return _normalize_phone('', phone)
