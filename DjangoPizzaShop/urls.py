from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', include('shop.urls', namespace='shop')),
    path('well-known/apple-developer-merchantid-domain-association/',
         TemplateView.as_view(template_name='shop/apple-developer-merchantid-domain-association')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_title = _('Admin index title')
admin.site.site_header = _('Admin site header')
admin.site.site_title = _('Admin title')
