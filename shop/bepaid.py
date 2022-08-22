import requests
from django.urls import reverse
from django.conf import settings
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger(__file__)


class Bepaid:
    def __init__(self):
        self.test = bool(settings.DEBUG)
        self.redirect_page = reverse('shop:shop-home')
        # self.redirect = absoluteuri.build_absolute_uri(self.redirect_page)
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
        response = requests.post(self.url, json=payload, headers={'Accept': 'application/json'}, auth=HTTPBasicAuth('3013', '85b45d21923689cae8026b90a5f832f2221bede68265b566b86cdfd7ba21de41'))
        # response.json()
        # if settings.DEBUG:
        #     print(f"bepaid redirection link: "+response.json().get('checkout').get('redirect_url'))
        logger.error(response.json())
        return response.json().get('checkout').get('redirect_url')
