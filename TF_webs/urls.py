"""TF_webs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin 
from . import view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^print$', view.co_print),
    url(r'^function$', view.func),
    url(r'^db_in$', view.db_in),
    url(r'^co_info$',view.co_info),
    url(r'^item_info$',view.item_info),
    url(r'^co_info/all_co$',view.all_co),
    url(r'^co_info/item_come$',view.item_come),
    url(r'^co_info/info_search$',view.info_search),
    url(r'^co_info/update_nums$',view.update_nums),
    url(r'^co_info/update_qy$',view.update_qy),
    url(r'^print/page1$',view.page1),
    url(r'^co_info/update_send$',view.update_send),
]