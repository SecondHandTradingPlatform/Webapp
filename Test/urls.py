"""Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from webapp.views import publish_goods
from webapp.views import admin_index, admin_users,admin_goods, admin_newgoods, admin_record
from webapp.views import admin_bulletin, admin_newbulletin, admin_rstpassword, admin_login
from webapp.views import admin_message, admin_remessage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('publish_goods/', publish_goods),
    path('admin_index/', admin_index),
    path('admin_users/', admin_users),
    path('admin_goods/', admin_goods),

    path('admin_newgoods/', admin_newgoods),
    path('admin_record/', admin_record),
    path('admin_bulletin/', admin_bulletin),
    path('admin_newbulletin/', admin_newbulletin),
    path('admin_rstpassword/', admin_rstpassword),
    path('admin_sign_in/', admin_login),
    path('', admin_login),
    path('admin_message/', admin_message),
    path('admin_remessage/', admin_remessage),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
