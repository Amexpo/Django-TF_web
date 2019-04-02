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
    url(r'^$', view.db_in),
    url(r'^db_in$', view.db_in),
    url(r'^TF$', view.db_in),
    url(r'^TF/db_in$', view.db_in),
    url(r'^TF/co_info$',view.co_info),
    url(r'^TF/co_info/all_co$',view.all_co),
    url(r'^TF/co_info/info_search$',view.info_search),
    url(r'^TF/co_info/update_qy$',view.update_qy),
    url(r'^TF/item_info$',view.item_info),
    url(r'^TF/item_info/item_come$',view.item_come),
    url(r'^TF/item_info/update_nums$',view.update_nums),
    url(r'^TF/item_info/update_send$',view.update_send),
    url(r'^TF/item_info/ItemManageNums$',view.ItemManageNums),
    url(r'^admin/', admin.site.urls),
    url(r'^TF/print$', view.co_print),
    url(r'^TF/print/page1$',view.page1),
    url(r'^TF/function$', view.func),
    url(r'^TF/rpm$', view.rpm),
    url(r'^TF/rpm/report$',view.report),
    url(r'^TF/rpm/CPList$',view.CPList),
    url(r'^TF/rpm/item/$',view.item),
    url(r'^TF/barcodeDJ/$',view.barcodeDJ),
    url(r'^TF/barcodeDJ/companyList$',view.barcodeDJ_companyList),
    url(r'^TF/barcodeDJ/consignList$',view.barcodeDJ_consignList),
    url(r'^label$',view.label_consign),
    url(r'^label/consign$',view.label_consign),
    url(r'^label/edit$',view.label_edit),
    url(r'^label/edit_list$',view.label_edit_list),
    url(r'^label/edit/record$',view.label_edit_record),
    url(r'^label/check$',view.label_check),
    url(r'^label/check_list$',view.label_check_list),
    url(r'^label/print$',view.label_print),
    url(r'^label/setting$',view.label_setting),
    url(r'^label/img$',view.pdf417)
]