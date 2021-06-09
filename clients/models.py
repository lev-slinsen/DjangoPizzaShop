from django.db import models
from django.conf import settings


class Company(models.Model):
    PAYMENT_CHOICES = [
        (0, 'Cash'),
        (1, 'Card'),
        (2, 'Online'),
    ]
    unp = models.CharField(max_length=30, verbose_name="UNP")
    name = models.CharField(max_length=30, verbose_name="Name")
    legal_address = models.CharField(max_length=50, verbose_name="Legal address")
    address_order = models.CharField(max_length=50, verbose_name="Delivery address")
    contact_person = models.CharField(max_length=50, verbose_name="The contact person")
    number = models.CharField(max_length=15, verbose_name="Number")
    note = models.TextField(max_length=2000, verbose_name="Note")
    email = models.CharField(max_length=50, verbose_name="Email")
    payment = models.SmallIntegerField(
        choices=PAYMENT_CHOICES,
        verbose_name="Payment format",
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    @classmethod
    def normalize_phone(cls, phone):
        """
        Remove extra spaces and non-digit chars from phone.
        """
        _normalize_phone = re.compile(r'(\s{2,}|[a-zA-Z]+)').sub
        return _normalize_phone('', phone)


class Customer(models.Model):
    """
    Custom user model.
    """
    phone = models.CharField(max_length=100, unique=True, verbose_name='Phone')
    first_name = models.CharField(max_length=30, verbose_name='Name')
    point = models.IntegerField(default=0, verbose_name='Point')

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