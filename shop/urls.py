from django.template.defaulttags import url
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views
from accounts import views as acc_views
from rest_framework import routers
from .settingTelegramBot import *

router = routers.DefaultRouter()
router.register('users/', acc_views.UserViewSet)
app_name = 'shop'


urlpatterns = [
    path('', views.home, name='shop-home'),
    path('about/', views.about, name='shop-about'),
    path('cart/', views.cart, name='shop-cart'),
    path('order/', views.order, name='shop-order'),
    path('legal_order/', views.legal_order, name='shop-legal-order'),
    path("robots.txt", TemplateView.as_view(template_name="shop/robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="shop/sitemap.xml")),
    path(f'webhook/{TOKEN_BOT}', views.webhook)
]
