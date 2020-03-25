"""DjangoPizzaShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
# from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.utils.translation import gettext_lazy as _


# urlpatterns = i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
#     path('', include('shop.urls')),
#     prefix_default_language=False
# ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', include('shop.urls', namespace='shop')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_title = _('Admin index title')
admin.site.site_header = _('Admin site header')
admin.site.site_title = _('Admin title')
