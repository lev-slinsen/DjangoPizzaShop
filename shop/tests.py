from decimal import Decimal

from django.test import TestCase
from catalog.models import Pizza, Category, Size
from .models import CompanyOrderItem, LegalOrder
from clients.models import Company
from django.core.files import File
from django.urls import reverse
import json


class LegalTest(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(
            unp='228143',
            name='Есити',
            address_legal='ул. Богдана 12',
            address_order='ул. Ветреная 44',
            contact_person='Алексей Пушкин',
            phone='37533619216',
            note='Булочная большая',
            email='demoh@gmail.com',
            payment=0,
        )
        category = Category.objects.create(
            name='70гр'
        )

        self.pizza1 = Pizza.objects.create(
            name='Мандарины',
            content='Большие',
            description='Мандарины из РБ',
            photo=File(file=b'')
        )
        self.pizza1.category.add(category)
        Size.objects.create(
            type='small',
            price=99,
            pizza=self.pizza1,
            active=True,
        )

        self.pizza2 = Pizza.objects.create(
            name='Творог',
            content='Маленькие',
            description='Без ГМО',
            photo=File(file=b'')
        )
        self.pizza2.category.add(category)
        Size.objects.create(
            type='small',
            price=50,
            pizza=self.pizza2,
            active=True,
        )

        self.pizza3 = Pizza.objects.create(
            name='Мандарины',
            content='Большие',
            description='Мандарины из РБ',
            photo=File(file=b'')
        )
        self.pizza3.category.add(category)
        Size.objects.create(
            type='large',
            price=80,
            pizza=self.pizza3,
            active=True,
        )

    def tearDown(self) -> None:
        CompanyOrderItem.objects.all().delete()
        LegalOrder.objects.all().delete()
        self.company.delete()
        self.pizza1.delete()
        self.pizza2.delete()
        self.pizza3.delete()
        Category.objects.all().delete()
        Size.objects.all().delete()

    def test_legal_order(self):
        data = {'delivery_date': ['2021-07-29'],
                'company': self.company.id,
                'legal_order': json.dumps(
                    [
                        {"size": "small", "quantity": 1, "id": self.pizza1.id},
                        {"size": "small", "quantity": 9, "id": self.pizza1.id},
                    ]
                )
                }

        response = self.client.post(reverse('shop:shop-legal-order'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LegalOrder.objects.count(), 1)
        self.assertEqual(CompanyOrderItem.objects.count(), 2)
        self.assertEqual(LegalOrder.objects.get(company=self.company).total_price(), Decimal('990.00'))

    def test_legal_order2(self):
        data = {'delivery_date': ['2021-07-29'],
                'company': self.company.id,
                'legal_order': json.dumps(
                    [
                        {"size": "small", "quantity": 5, "id": self.pizza1.id},
                        {"size": "small", "quantity": 5, "id": self.pizza2.id},
                    ]
                )
                }

        response = self.client.post(reverse('shop:shop-legal-order'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LegalOrder.objects.count(), 1)
        self.assertEqual(CompanyOrderItem.objects.count(), 2)
        self.assertEqual(LegalOrder.objects.get(company=self.company).total_price(), Decimal('745.00'))

    def test_legal_order3(self):
        data = {'delivery_date': ['2021-07-29'],
                'company': self.company.id,
                'legal_order': json.dumps(
                    [
                        {"size": "small", "quantity": 4, "id": self.pizza1.id},
                        {"size": "small", "quantity": 5, "id": self.pizza2.id},
                        {"size": "large", "quantity": 7, "id": self.pizza3.id},
                    ]
                )
                }

        response = self.client.post(reverse('shop:shop-legal-order'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LegalOrder.objects.count(), 1)
        self.assertEqual(CompanyOrderItem.objects.count(), 3)
        self.assertEqual(LegalOrder.objects.get(company=self.company).total_price(), Decimal('1206.00'))

    def test_legal_order4(self):
        data = {'delivery_date': ['2021-07-29'],
                'company': self.company.id,
                'legal_order': json.dumps(
                    [
                        {"size": "small", "quantity": 0, "id": self.pizza1.id},
                        {"size": "small", "quantity": 0, "id": self.pizza2.id},
                        {"size": "large", "quantity": 1, "id": self.pizza3.id},
                    ]
                )
                }

        response = self.client.post(reverse('shop:shop-legal-order'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LegalOrder.objects.count(), 1)
        self.assertEqual(CompanyOrderItem.objects.count(), 3)
        self.assertEqual(LegalOrder.objects.get(company=self.company).total_price(), Decimal('80.00'))

    def test_legal_order_empty(self):
        data = {'delivery_date': ['2021-07-29'],
                'company': self.company.id,
                'legal_order': json.dumps([])
                }

        response = self.client.post(reverse('shop:shop-legal-order'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LegalOrder.objects.count(), 0)
        self.assertEqual(CompanyOrderItem.objects.count(), 0)

    def test_legal_order_empty_form(self):
        data = {'delivery_date': '',
                'company': '',
                'legal_order': json.dumps(
                    [
                        {"size": "small", "quantity": 1, "id": 1},
                        {"size": "small", "quantity": 9, "id": 1},
                    ]
                )
                }

        response = self.client.post(reverse('shop:shop-legal-order'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LegalOrder.objects.count(), 0)
        self.assertEqual(CompanyOrderItem.objects.count(), 0)
