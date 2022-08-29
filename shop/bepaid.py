import logging

import requests
from django.conf import settings
from django.urls import reverse
from requests.auth import HTTPBasicAuth
import os

logger = logging.getLogger(__file__)


class Bepaid:
    def __init__(self):
        self.test = settings.DEBUG
        logging.error(settings.DEBUG)
        logging.error(settings.ENABLE_LOGGING)
        logging.error(os.environ.get('DJANGO_DEBUG'))
        logging.error(bool(os.environ.get('DJANGO_DEBUG', False)))
        self.redirect_page = reverse('shop:shop-home')
        self.redirect = 'http://pechorin.by'
        self.url = 'https://checkout.bepaid.by/ctp/api/checkouts'
        self.auth = ('user', 'passwd')

    def bp_token(self, total_price):
        payload = {
            "checkout": {
                "version": 2.1,
                "test": self.test,
                "transaction_type": "payment",
                "attempts": 3,
                "settings": {
                    "success_url": self.redirect,
                    "decline_url": self.redirect,
                    "fail_url": self.redirect,
                    "cancel_url": self.redirect,
                    "notification_url": self.redirect,
                    "button_text": "Оплатить",
                    "button_next_text": "Вернуться в магазин",
                    "language": "ru",
                },
                "order": {
                    "currency": "BYN",
                    "amount": total_price,
                    "description": 'После совершения оплаты, мы перезвоним Вам для подтверждения заказа. Пекарня "Печорин"'
                },
            }
        }
        logging.error(payload)
        response = requests.post(self.url, json=payload, headers={'Accept': 'application/json'}, auth=HTTPBasicAuth('3013', '85b45d21923689cae8026b90a5f832f2221bede68265b566b86cdfd7ba21de41'))
        logging.error(response)
        return response.json().get('checkout').get('redirect_url')
