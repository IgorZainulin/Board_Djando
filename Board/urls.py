"""
URL configuration for Bulletin_Board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static

from django.views.generic import TemplateView

#
# from rest_framework import routers
# from news import viewsets
#
# router = routers.DefaultRouter()
# router.register(r'news', viewsets.NewsViewset)


urlpatterns = [
   path('admin/', admin.site.urls),

   # path('swagger-ui/', TemplateView.as_view(
   #    template_name='swagger-ui.html',
   #    extra_context={'schema_url': 'openapi-schema'}
   # ), name='swagger-ui'),

   path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
   # подключались к главному приложению с префиксом products/.
   path('advertisement/', include('advertisement.urls')),


   # path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные)
   #
   # path('api/', include(router.urls)),
   # # path('api-own/', include('appi.urls')),
   path('ckeditor/', include('ckeditor_uploader.urls')),
   # path("", include("advertisement.urls")),

   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
]

